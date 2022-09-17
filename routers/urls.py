from django.urls import path, include



urlpatterns = [
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
]
