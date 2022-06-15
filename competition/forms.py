
from django import forms

from .models import Competition


class NewCompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('winners_enabled',)