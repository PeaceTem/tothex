from django.db import models
from django.contrib.auth.models import User
from core.models import Streak
# Create your models here.
"""
The list of leaderboard models that will be created.
It should be specific to a country. Still considering.
streak
best question
best quiz
top earners
top buyers
top losers if the challenges have started.
most answered questions
most correctly answered questions
most wrongly answered questions
most attempted questions



Save the state of the streak leader board at the end of each week for future analysis.
"""

#new instance will be created every week
class StreakLeaderBoard(models.Model):
    leaders = models.ManyToManyField(Streak, related_name='leaders')
    date = models.DateField(auto_now_add=True)
    week = models.PositiveSmallIntegerField(default=0)

    # add a property or a function that will get the id of the lastest instance of this model

    @property
    def lastestModel(self):
        return self.id

    def __str__(self):
        return f"{self.id}"




class CoinEarnerLeaderBoard(models.Model):
    leaders = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    # The order_by will be used in the views to get the highest coins earners
    # add the leaderboard for the all time highest coins owner



    def __str__(self):
        return f"{self.id}"