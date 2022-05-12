from django.urls import path
from . import views


app_name = 'leaderboard'


urlpatterns = [
    # quiz question leaderboard profile wallet
    # add the leaderboard in the navigation bar
    path('leaderboard/', views.Leaderboard, name='leaderboard'),
    path('streak/', views.StreakLeaderBoard, name='streak'),
    path('wealth/', views.WealthLeaderBoard, name='wealth'),
    path('referral/', views.ReferralLeaderBoard, name='referral'),
    path('creator/', views.CreatorsLeaderBoard, name='creator'),

]

