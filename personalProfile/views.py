from django.shortcuts import render, get_object_or_404, redirect
from core.models import Profile, Follower, Link, Interest
from django.contrib.auth.models import User
from django.db.models import Count, Q
from quiz.models import Quiz
from question.models import TrueOrFalseQuestion, FourChoicesQuestion

from core.forms import NewInterestReportForm
# Create your views here.


def MassProfile(request, profile_name):
    try:
        user = User.objects.select_related('profile').get(username=profile_name)
        profile = user.profile
        link = Link.objects.get(profile=profile)
        
        follower = Follower.objects.prefetch_related('followers','following').get(user=user)
        followersCount = follower.followers.all().count()
        followingsCount = follower.following.all().count()
        # follower = Follower.objects.annotate(followersCount=followersCount).annotate(followingsCount=followingsCount)
        print(follower)
        if user != request.user:
            profile.views += 1
            profile.save()

        form = NewInterestReportForm()
        
        
    except:
        return redirect('quiz:quizzes')
    
    context = {
        'profile': profile,
        'follower' : follower,
        'link': link,
        'nav': 'profile',
        'followersCount': followersCount,
        'followingsCount': followingsCount,
        'form': form,
    }

    return render(request, 'core/profile.html', context)
