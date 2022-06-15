from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('login/', views.CustomLoginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='account_login'), name='logout'),

    #essentials
    path('privacy-policy/', views.PrivacyPolicy, name='privacy-policy'),
    path('terms-and-conditions/', views.TermsAndConditions, name='terms-and-conditions'),


    #referral
    path('', views.Home, name='home'),
    path('menu/', views.Menu, name='menu'),

    path('referral/<str:ref_code>/', views.main_view, name='main_view'),
    path('profiles/', views.my_recommendations_view, name='my_recs_view'),

    #followers 
    path('profile/follower', views.FollowView, name='follower'),
    path('profile/unfollow', views.UnfollowView, name='unfollow'),
    path('profile/followerlist/<str:follower_id>/<str:page_name>/', views.FollowerListView, name='follower-list'),

    # link clicks
    path('profile/link-click/<str:link_id>', views.LinkClick, name='link-click'),


    # interest 
    path('interest/', views.InterestReport, name='interest'),


    #change password
    path('password/',views.PasswordsChangeView.as_view(), name='change_password'),
    path('password_success', views.password_success, name='password_success'),

    #reset password
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'),
    name='reset_password'),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='core/reset_password_sent.html'),
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_form.html'),
    name='password_reset_confirm'),

    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
    name='password_reset_complete'),

    # profile
    path('profile/', views.ProfilePage, name='profile'),
    path('edit_profile/', views.ProfileCreationPage, name='edit_profile'),

    # link
    path('edit-link/', views.EditLink, name='edit-link'),
]
