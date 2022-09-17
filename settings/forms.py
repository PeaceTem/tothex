from django.contrib.auth.models import User

# from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


"""
widgets = forms.Textarea, forms.TextInput(attrs={'class':'input-class'}), forms.Select
required = bool

add multiple choice field for category in subcategory page 256


FilePathField

"""

class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(widget=forms.TextInput(), label=_("New Username"))
    confirm_new_username = forms.CharField(widget=forms.TextInput(), label=_("Confirm New Username"))



class PasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label=_("New Password"))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(), label=_("Confirm New Password"))
