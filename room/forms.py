from django import forms
from .models import StudyRoom, Announcement



class StudyRoomForm(forms.Form):
    class Meta:
        model = StudyRoom
        fields = ('name',)


class AnnouncementForm(forms.Form):
    class Meta:
        model = Announcement
        fields = ('announcement',)