


from django.db import models
from django.contrib.auth.models import User
from core.models import Streak
# Create your models here.
"""
The list of leaderboard models that will be created.
It should be specific to a country. Still considering.
streak

Save the state of the streak leader board at the end of each week for future analysis.
"""


"""
Add the signals for the leaderboard
"""


class CoinsEarnerLeaderBoard(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    # The order_by will be used in the views to get the highest coins earners
    # add the leaderboard for the all time highest coins owner



    def __str__(self):
        return f"{self.leader}"





class CreatorLeaderBoard(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    # The order_by will be used in the views to get the highest coins earners
    # add the leaderboard for the all time highest coins owner



    def __str__(self):
        return f"{self.leader}"




class ReferralLeaderBoard(models.Model):
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    refers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.leader}"