from django.shortcuts import render
from core.models import Streak, Profile
from django.contrib.auth.decorators import login_required

from .models import CoinsEarnerLeaderBoard, CreatorLeaderBoard, ReferralLeaderBoard
# Create your views here.


"""
Add Pagination To All The Leaderboard

And also make all the leaderboard daily
"""




# @login_required(redirect_field_name='next', login_url='account_login')
def LeaderboardView(request):
    user = request.user
    profile = None
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
    context={
        'nav': 'leaderboard',
        'profile': profile,
    }
    return render(request, 'leaderboard/leaderboard.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def StreakLeaderBoardView(request):
    user = request.user
    profile = user.profile
    instance = Streak.objects.get(profile=profile)
    leaders = Streak.objects.all().order_by('-length', '-question')[0:100]
    index = (*leaders,).index(instance) + 1 or "1000+"
    # add the get absolute url function to the profile
    # add pagination and waypoint or ajax I think Ajax will be more controllable
    # index = 1
    context = {
        'leaders': leaders,
        'index': index,
        'instance' : instance,
    }

    return render(request, 'leaderboard/streak.html', context)


# add the function for reward that will be triggered by celery. it wont't be a view function



@login_required(redirect_field_name='next', login_url='account_login')
def WealthLeaderBoardView(request,*args, **kwargs):
    user = request.user
    instance = CoinsEarnerLeaderBoard.objects.get(leader=user)
    leaders = CoinsEarnerLeaderBoard.objects.all().order_by('-coins')[0:100]
    index = (*leaders,).index(instance) + 1 or "1000+"
    context = {
        'leaders' : leaders,
        'index': index,
        'instance' : instance,
    }

    return render(request, 'leaderboard/wealth.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def CreatorsLeaderBoardView(request,*args, **kwargs):
    user = request.user
    instance = CreatorLeaderBoard.objects.get(leader=user)
    leaders = CreatorLeaderBoard.objects.all().order_by('-coins')[0:100]
    index = (*leaders,).index(instance) + 1 or "1000+"

    context = {
        'leaders' : leaders,
        'index': index,
        'instance' : instance,
    }

    return render(request, 'leaderboard/wealth.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def ReferralLeaderBoardView(request,*args, **kwargs):
    user = request.user
    leaders = ReferralLeaderBoard.objects.all().order_by('-refers')[0:100]
    instance = ReferralLeaderBoard.objects.get(leader=user)

    index = (*leaders,).index(instance) + 1 or "1000+"

    context = {
        'leaders' : leaders,
        'index': index,
        'instance' : instance,
    }

    return render(request, 'leaderboard/referral.html', context)





