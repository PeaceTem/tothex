from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from quiz.models import Quiz
# Create your models here.





class Competition(models.Model):
    quiz = models.OneToOnefield(Quiz, on_delete=models.CASCADE)
    takers = models.ManyToManyField(User, blank=True,null=True)
    prize = models.FloatField(default=0)
    winners_enabled = models.PositiveIntegerField(default=0)
    winners = models.ManyToManyField(User, blank=True, null=True)
    active = models.BooleanField(default=True)

