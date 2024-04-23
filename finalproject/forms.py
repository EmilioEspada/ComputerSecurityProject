from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import *


# Form inherited from TicketMaster project
class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to the widgets
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


# Form inherited from TicketMaster project
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Customize the list of fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control m-2'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control m-2'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control m-2'})


# Form that is called upon saving a note: Form made by William
class SavedNotesForm(forms.ModelForm):

    # sends all data to form except user, username, date, and time
    class Meta:
        model = SavedNotes
        exclude = ('user', 'username', 'date', 'time')


# Form that is called upon sending a note: Form made by William
class SendNotesForm(forms.Form):
    # custom form that takes a username for the user to send to
    Username = forms.CharField(max_length=100)
