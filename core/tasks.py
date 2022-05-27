from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import Streak, Profile, Device
from quiz.models import Quiz
from leaderboard.models import CoinsEarnerLeaderBoard, ReferralLeaderBoard, CreatorLeaderBoard

from django.utils import timezone


@shared_task
def add(x: int , y: int):
    return x + y



@shared_task
def DailyStreakUpdate():

    '''
    Add an email to send to those that won in the leaderboard
    Let people know that any message will be relayed through their emails.
    '''


    Streak.objects.all().update(question=0, active=False)
    #award all the coins in here
    earners_leaders = CoinsEarnerLeaderboard.objects.select_related('leader').filter(coins__gte=50).order_by('-coins')[:100]
    for earner in earners_leaders:
        user=earner.leader
        profile= Profile.objects.get(user=user)
        profile.coins += 500
        profile.save()
    CoinsEarnerLeaderboard.objects.all().update(coins=0)    
    
    
    
    refers_leaders = ReferralLeaderBoard.objects.select_related('leader').filter(refers__gte=1).order_by('-coins')[:100]
    for earner in refers_leaders:
        user=earner.leader
        profile= Profile.objects.get(user=user)
        profile.coins += 500
        profile.save()
    ReferralLeaderBoard.objects.all().update(refers=0)


    creators_leaders = CreatorLeaderBoard.objects.select_related('leader').filter(refers__gte=1).order_by('-coins')[:100]
    for earner in creators_leaders:
        user=earner.leader
        profile= Profile.objects.get(user=user)
        profile.coins += 500
        profile.save()
    CreatorLeaderBoard.objects.all().update(refers=0)


    devices = Device.objects.all().count()
    tm = timezone.now()
    for device in devices:
        td =(tm - device.date).days

        if td >= 30:
            device.delete()

    return "All the streak model has been updated!"




@shared_task
def LikeQuiz(quiz_id, user):
    user = user
    quiz = Quiz.objects.select_related('user').prefetch_related('likes').get(id=quiz_id)
    profile = Profile.objects.get(user=quiz.user)
    likeProfile = Profile.objects.prefetch_related('favoriteQuizzes').get(user=user)
    
    if user in quiz.likes.all():
        quiz.likes.remove(user)
        quiz.likeCount -= 1
        profile.likes -= 1
        likeProfile.favoriteQuizzes.remove(quiz)
        likeProfile.save()
        quiz.save()
        profile.save()
        return HttpResponse('unliked')

    else:
        quiz.likes.add(user)
        profile.likes += 1
        quiz.likeCount += 1
        likeProfile.favoriteQuizzes.add(quiz)
        quiz.save()
        profile.save()

        return HttpResponse('liked')



@shared_task
def StreakValidator(profile, value):
    streak = Streak.objects.get(profile=profile)
    streak.validateStreak(value)

    return "The Streak has been successfully validated"



@shared_task
def CoinsTransaction(user, coins):
    leader = CoinsEarnerLeaderBoard.objects.get(leader=user)
    leader.coins += coins
    leader.save()

    return "Coin Transaction Task is Successful"


@shared_task
def CreatorCoins(user, coins):
    # change this to the creator
    leader = CreatorLeaderBoard.objects.get(leader=user)
    leader.coins += coins
    leader.save()

    return "Coin Transaction Task is Successful"



@shared_task
def ReferralTask(user):
    print("Starting Task")
    leader = ReferralLeaderBoard.objects.get(leader=user)
    leader.refers += 1
    leader.save()
    print("Ending Task")

    return "Referral Task is Successful"



"""
Check everything about the leaderboard models patapata

"""



# add all the background tasks for like, solution_quality, validate streak, emails, transactions


# celery -A student worker -l info
# add.apply async{(3,3), countdown=5}
# install django-celery-beat
# and add it to the instailed apps. "django_celery_beat"
# migrate


"""
CELERY_BEAT_SCHEDULE = {
    "scheduled_tasks" :{
        'task' : 'core.tasks.add',
        'schedule' : 10.0 or crontab(minute=0, hour=0),
        'args' : (10,10),
    },
    "dailyStreakUpdate" : {
        task' : 'core.tasks.DailyStreakUpdate',
        'schedule' : crontab(minute=0, hour=0),   
    }
}
solution to failure in celery task or time.sleep(1)
task_send_welcome_email.apply_async(args=[user.pk], countdown=10)

Research if it is good to use atomic requests
"""


"""

# task.py


from celery.decorators import task

@task(name="send_review_email_task")




# views.py 
def send_email():
    send_review_email_task.delay(name,email,review)



# email.py

from django.template import Context
from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from django.conf import settings




def send_review_email(name,email,review):
    context={
        "name":name,
        "email":email,
        "review":review,
    }




    email_subject = "Thank you for the review!"



    """