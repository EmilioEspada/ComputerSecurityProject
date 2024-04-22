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


# Form made by William
class SavedNotesForm(forms.ModelForm):
    class Meta:
        model = SavedNotes
        exclude = ('user', 'username', 'date', 'time')


# Form made by William
class SendNotesForm(forms.Form):
    Username = forms.CharField(max_length=100)
