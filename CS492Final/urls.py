"""
URL configuration for CS492Final project.
Inherited from TicketMaser project, some parts made by Django.
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
from django.views.generic import RedirectView

from finalproject import views
from finalproject.views import signup

# Inherited from TicketMaster project, additions made by William
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/signup/'), name='redirect_to_signup'),
    path('signup/', signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('view-notes/', views.view_notes, name='view-notes'),
    path('update/<int:note_id>', views.update_note, name='update-note'),
    path('create-note/', views.create_note, name='create-note'),
    path('delete/<int:id>', views.delete_note, name='delete-note'),
    path('updateNote/<int:note_id>', views.update_comp_note, name='update-comp-note'),
    path('sendNote/<int:note_id>', views.send_note, name='send-note'),

    # used to test encryption, not needed for final product
    path('test-crypto/', views.test_crypto, name='test-crypto'),
]
