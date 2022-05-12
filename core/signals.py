
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Streak, Follower, Link
from leaderboard.models import CoinsEarnerLeaderBoard, ReferralLeaderBoard
from category.models import Category
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

"""
Whenever a user is created, loop through the sessionstore
"""


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        quizCategories = Category.objects.all().order_by('-quiz_number_of_times_taken')[:5]
        questionCategories = Category.objects.all().order_by('-question_number_of_times_taken')[:5]
        for category in quizCategories:
            profile.categories.add(category)

        for category in questionCategories:
            profile.categories.add(category)
            profile.save()
        CoinsEarnerLeaderBoard.objects.create(leader=instance)
        ReferralLeaderBoard.objects.create(leader=instance)
        Follower.objects.create(user=instance)



@receiver(post_save, sender=User)
def update_profile(sender, instance, created, *args, **kwargs):
    if not created:
        profile = instance.profile
        username = instance.username
        profile.code = username
        profile.save()
        print('profile updated!')

# post_save.connect(create_profile, sender=User)

# @receiver(post_save, sender=User)
# def update_profile(sender, instance, created, *args, **kwargs):
#     if created == False:
#         instance.profile.save()
        
# post_save.connect(update_profile, sender=User)


@receiver(post_save, sender=Profile)
def create_streak(sender, instance, created, *args, **kwargs):
    if created:
        # add the referral code here
        Link.objects.create(profile=instance)
        Streak.objects.create(profile=instance)


# This should be called update_streak





