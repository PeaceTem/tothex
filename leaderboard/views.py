from django.shortcuts import render
from core.models import Streak, Profile
from django.contrib.auth.decorators import login_required

from .models import CoinsEarnerLeaderBoard, CreatorLeaderBoard, ReferralLeaderBoard
# Create your views here.


"""
Add Pagination To All The Leaderboard

And also make all the leaderboard daily
"""




@login_required(redirect_field_name='next', login_url='account_login')
def Leaderboard(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context={
        'nav': 'leaderboard',
        'profile': profile,
    }
    return render(request, 'leaderboard/leaderboard.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def StreakLeaderBoard(request):
    leaders = Streak.objects.all().order_by('-length', '-question')[0:1000]
    # add the get absolute url function to the profile
    # add pagination and waypoint or ajax I think Ajax will be more controllable

    context = {
        'leaders': leaders,
    }

    return render(request, 'leaderboard/streak.html', context)


# add the function for reward that will be triggered by celery. it wont't be a view function



@login_required(redirect_field_name='next', login_url='account_login')
def WealthLeaderBoard(request,*args, **kwargs):
    leaders = CoinsEarnerLeaderBoard.objects.all().order_by('-coins')[0:1000]
    context = {
        'leaders' : leaders,
    }

    return render(request, 'leaderboard/wealth.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def CreatorsLeaderBoard(request,*args, **kwargs):
    leaders = CreatorLeaderBoard.objects.all().order_by('-coins')[0:1000]
    context = {
        'leaders' : leaders,
    }

    return render(request, 'leaderboard/wealth.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def ReferralLeaderBoard(request,*args, **kwargs):
    leaders = ReferralLeaderBoard.objects.all().order_by('-refers')
    context = {
        'leaders' : leaders,
    }

    return render(request, 'leaderboard/referral.html', context)





