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
        user = request.user
        owner = User.objects.get(username=profile_name)
        profile = Profile.objects.select_related("user","streak").get(user=owner)
        link = Link.objects.get(profile=profile)
        
        follower = Follower.objects.prefetch_related('followers','following').get(user=owner)
        followersCount = follower.followers.all().count()
        followingsCount = follower.following.all().count()
        if user != owner:
            profile.views += 1
            profile.save()

        form = NewInterestReportForm()
        
        
    except:
        return redirect('quiz:quizzes')
    
    context = {
        'user': user,
        'profile': profile,
        'follower' : follower,
        'link': link,
        'nav': 'profile',
        'followersCount': followersCount,
        'followingsCount': followingsCount,
        'form': form,
    }

    return render(request, 'core/profile.html', context)
