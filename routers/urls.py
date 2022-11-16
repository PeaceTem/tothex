from django.urls import path, include
from django.shortcuts import render

def HomePage(request):
    user = request.user
    profile = None
    try:
        profile = user.profile
    except:
        pass
    context = {
        "profile" : profile,
    }
    return render(request, 'home.html', context)



urlpatterns = [
    path('', HomePage),
    path('accounts/', include('allauth.urls')),
    path('core/', include('core.urls')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
    path('category/', include('category.urls', namespace='category')),
    path('question/', include('question.urls', namespace='question')),
    path('leaderboard/', include('leaderboard.urls', namespace='leaderboard')),
    path('@', include('personalProfile.urls', namespace='profile')),
    path('ads/', include('ads.urls', namespace='ads')),
    path('qxa/', include('q.urls', namespace='qxa')),
    path('settings/', include('settings.urls', namespace='settings')),
    path('room/', include('room.urls', namespace='room')),
]
