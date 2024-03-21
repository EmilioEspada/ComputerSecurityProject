from datetime import datetime

import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import SavedEvents


@login_required()
def search(request):
    if request.POST.get('search'):
        classification_name = request.POST['classification_name']
        city = request.POST['city']
        sort = "date,asc"

        if not classification_name:
            messages.info(request, 'Search term cannot be empty. Please enter a search term.')
            return redirect('search-results')
        elif not city:
            messages.info(request, 'City cannot be empty. Please enter a city.')
            return redirect('search-results')

        search_results = get_ticketmaster_search(classification_name, city, sort)
        if search_results is None:
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            return redirect('search-results')

        events_found = search_results['page']['totalElements']
        if events_found > 20:
            events_found = 20  # the ticketMasterAPI only allows 20 results per page by default

        if events_found == 0:
            messages.info(request, 'Sorry... no results were found for the entered search term and city.')
            return redirect('search-results')

        else:
            events = search_results['_embedded']['events']
            event_list = []
            for event in events:
                event_name = event['name']
                event_image = event['images'][0]['url']
                for image in event['images']:
                    if image['height'] == 1152:
                        event_image = image['url']

                #  Some events don't have a date or time, so return nothing if one of these events show up
                try:
                    event_date = event['dates']['start']['dateTime']
                    date_object = datetime.strptime(event_date[:10], "%Y-%m-%d")
                    event_date = date_object.strftime("%a %b %d %Y")
                except KeyError:
                    event_date = ""
                try:
                    event_time = event['dates']['start']['localTime']
                    event_time = event_time[:-4]
                    time_object = datetime.strptime(event_time, "%H:%M")
                    event_time = time_object.strftime("%I:%M %p")
                except KeyError:
                    event_time = ""

                venue = event['_embedded']['venues'][0]
                venue_name = venue['name']
                venue_city = venue['city']['name']
                venue_state = venue['state']['name']
                venue_address = venue['address']['line1']
                ticket_link = event['url']

                event_details = {
                    'event_name': event_name,
                    'event_image': event_image,
                    'event_date': event_date,
                    'event_time': event_time,
                    'venue_name': venue_name,
                    'venue_city': venue_city,
                    'venue_state': venue_state,
                    'venue_address': venue_address,
                    'ticket_link': ticket_link,
                    'form': SavedEventsForm(initial={
                        'name': event_name,
                        'image': event_image,
                        'date': event_date,
                        'time': event_time,
                        'venue': venue_name,
                        'city': venue_city,
                        'state': venue_state,
                        'address': venue_address,
                        'link': ticket_link,
                        'favorite': None
                    })
                }
                event_list.append(event_details)

            context = {'events': event_list, 'events_found': events_found}

            return render(request, 'search-results.html', context)

    return render(request, 'search-results.html')


def logout_view(request):
    # This is the method to log out the user
    logout(request)
    # redirect the user to index page after logout
    return redirect('login')


def get_ticketmaster_search(classification_name, city, sort):
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=uR0EVsl1GNv6kaCf2DggXqQURjGEw1fe"
        params = {
            "classificationName": classification_name,
            "city": city,
            "sort": sort,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def signup(request):
    if request.user.is_authenticated:
        return redirect('search-results')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You are now logged in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'landing.html', context)


@login_required(login_url='login')
def view_events(request):  # view saved events
    events = SavedEvents.objects.filter(user=request.user)
    context = {'events': events}
    return render(request, 'saved-events.html', context)


@login_required(login_url='login')
def add_event(request):
    form = SavedEventsForm(request.POST or None)

    if request.method == 'POST':
        # Check if a similar event already exists in the database
        similar_events = SavedEvents.objects.filter(
            user=request.user,
            name=form.data.get('name'),
            date=form.data.get('date'),
            venue=form.data.get('venue'),
            city=form.data.get('city'),
            state=form.data.get('state'),
            address=form.data.get('address'),
            link=form.data.get('link'),
        )

        if similar_events.exists():
            # Handle the case when a similar event already exists
            return render(request, 'event_exists.html')

        # If no similar event exists and the form is valid, proceed with saving the new event
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('view-events')

    return render(request, 'search-results.html', {'form': form})


@login_required(login_url='login')
def update_event(request, event_id):  # favorite events that are saved
    event = SavedEvents.objects.get(id=event_id, user=request.user)
    form = SavedEventsForm(request.POST or None, instance=event)
    favorite = form.save(commit=False)
    favorite.favorite = 1 - favorite.favorite  # swaps between true and false whenever favorite is clicked
    favorite.save()
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('view-events')
    events = SavedEvents.objects.filter(user=request.user)
    context = {'events': events}
    return render(request, 'saved-events.html', context)


def login_view(request):
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('search-results')
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def delete_event(request, id):  # delete events from saved database
    event = SavedEvents.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('view-events')
    return render(request, 'delete-confirm.html', {'event': event})
