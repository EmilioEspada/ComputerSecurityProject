"""
URL configuration for CS492Final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from finalproject import views
from django.contrib.auth.views import LoginView
from finalproject.forms import BootstrapAuthenticationForm
from django.views.generic import RedirectView
from finalproject.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/signup/'), name='redirect_to_signup'),
    path('signup/', signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('search-results/', views.search, name='search-results'),
    path('add-event/', views.add_event, name='add-event'),  # C, add events to database
    path('view-events/', views.view_events, name='view-events'),  # R, retrieve events from database to view
    path('update/<int:event_id>', views.update_event, name='update-event'),  # U, update event to favorites or unfavorite
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:id>', views.delete_event, name='delete-event'),  # D, delete event from saved events database
]
