from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('list/', views.CategoryList.as_view(), name='category-list'),
    path('detail/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
]


