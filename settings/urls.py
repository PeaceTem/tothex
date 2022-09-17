from django.urls import path
from . import views

app_name='settings'
urlpatterns = [
    path('', views.Settings.as_view(), name='settings'),
    path('accounts/change-password.html', views.SetPassword.as_view(), name='change-password'),
    path('accounts/change-username.html', views.ChangeUsername.as_view(), name='change-username'),
    path('accounts/change-categories.html', views.EditProfileCategory.as_view(), name='change-categories'),
    # you might change this section to profile from accounts
    path('accounts/add-category-to-profile', views.AddProfileCategory.as_view(), name='add-profile-category'),
    path('accounts/remove-category-to-profile', views.RemoveProfileCategory.as_view(), name='remove-profile-category'),

]