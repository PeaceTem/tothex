from django.urls import path
from .views import ( Home, password_success, PasswordsChangeView, main_view,
my_recommendations_view, CustomLoginView, RegisterPage, ProfilePage,
ProfileCreationPage, FollowerView, UnfollowView)
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='account_login'), name='logout'),

    #referral
    path('', Home, name='home'),
    path('menu/', views.Menu, name='menu'),

    path('referral/<str:ref_code>/', main_view, name='main_view'),
    path('profiles/', my_recommendations_view, name='my_recs_view'),

    #followers 
    path('profile/follower', FollowerView, name='follower'),
    path('profile/unfollow', UnfollowView, name='unfollow'),

    # link clicks
    path('profile/link-click/<str:link_id>', views.LinkClick, name='link-click'),


    # interest 
    path('interest/', views.InterestReport, name='interest'),


    #change password
    path('password/',PasswordsChangeView.as_view(), name='change_password'),
    path('password_success', password_success, name='password_success'),

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
    path('profile/', ProfilePage, name='profile'),
    path('edit_profile/', ProfileCreationPage, name='edit_profile'),

    # link
    path('edit-link/', views.EditLink, name='edit-link'),
]
