from django.urls import path
from . import views


app_name = 'leaderboard'


urlpatterns = [
    # quiz question leaderboard profile wallet
    # add the leaderboard in the navigation bar
    path('leaderboard/', views.LeaderboardView, name='leaderboard'),
    path('streak/', views.StreakLeaderBoardView, name='streak'),
    path('wealth/', views.WealthLeaderBoardView, name='wealth'),
    path('referral/', views.ReferralLeaderBoardView, name='referral'),
    path('creator/', views.CreatorsLeaderBoardView, name='creator'),
    path('referrals/', views.referrals, name='referrals'),

]

