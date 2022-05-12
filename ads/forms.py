from django import forms

from .models import PostAd

class NewPostAdForm(forms.ModelForm):
    class Meta:
        model = PostAd
        fields = '__all__'