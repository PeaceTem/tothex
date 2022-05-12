from django.urls import path
from . import views

app_name='ads'

urlpatterns = [
    path('postAd/<str:nextpage>/', views.PostAdView, name='postAd'),
    path('postAd/click/<int:post_id>/<str:location>/', views.PostAdClick, name='post-click'),
]