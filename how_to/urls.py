from django.urls import path
from . import views

app_name='how_to'
urlpatterns = [
    path('', views.HowTo.as_view(), name='how-to'),

]