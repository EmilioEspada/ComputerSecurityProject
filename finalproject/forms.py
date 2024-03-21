from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class SearchForm(forms.ModelForm):
    class Meta:
        widgets = {
            'param1': forms.TextInput(attrs={
                'name': 'param1',
                'placeholder': 'Search by genre, artist or event',
                'type': 'text',
                'aria-label': 'keywords',
                'class': 'form-control'

            }),
            'param2': forms.TextInput(attrs={
                'name': 'param2',
                'placeholder': 'Enter a city e.g., Hartford',
                'type': 'text',
                'aria-label': 'keywords',
                'class': 'form-control'
            }),
        }


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to the widgets
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Customize the list of fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control m-2'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control m-2'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control m-2'})


class SavedEventsForm(forms.ModelForm):
    class Meta:
        model = SavedEvents
        exclude = ['user']
