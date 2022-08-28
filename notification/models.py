from django.db import models
from core.models import Profile
# Create your models here.

class Notification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    link = models.URLField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text