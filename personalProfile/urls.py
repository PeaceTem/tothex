from django.urls import path

from . import views


app_name = 'profile'

urlpatterns = [
    path('<str:profile_name>/', views.MassProfile, name='profile'),
]