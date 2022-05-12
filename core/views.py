from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse

# function based views
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, date, time, timedelta

from .models import Profile, Follower, Link, Interest
from .forms import ProfileCreationForm, LoginForm, NewLinkForm, NewInterestReportForm
from quiz.models import Quiz
from question.models import TrueOrFalseQuestion, FourChoicesQuestion




# services

from .services import ReferralService
# # Create your views here.
# messages.error, warning, success, info, debug
 

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

def Menu(request):
    return render(request, 'menu.html')

def Home(request):
    return render(request, 'core/home.html', {})

"""
Use try except block to catch errors

Change the streak coins to 5

Add a leaderboard about the longest running streak
"""
def main_view(request, *args, **kwargs):
    """
    Check if the Ip address has visited this page before and validate
    """
    user = request.user
    if not user.is_authenticated:
        code = str(kwargs.get('ref_code'))
        ReferralService(code)
    return redirect('question:answer-question')


def my_recommendations_view(request):
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommended_profiles()
    context = {
        'my_recs': my_recs,
    }
    return render(request, 'core/recommendation.html', context)



def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            page = request.user.userPageCounter or ''
            if not page:
                print('The user was deleted')
                request.user.delete()
            login(request, user)
            return redirect('quiz:quizzes')
        else:
            messages.error(request, 'Username or password does not exist')

    form = LoginForm()
    context={
        'form': form,
    }
    return render(request, 'core/login.html',context)


# user registration form
class RegisterPage(FormView):
    template_name = 'core/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('quiz:quizzes')


    def form_invalid(self, form):
        messages.error(self.request, "Your password can't be too similar to your other personal information.")
        messages.error(self.request, "Your password must contain at least 8 characters.")
        messages.error(self.request, "Your password can't be a commonly used password.")
        messages.error(self.request, "Your password can't be entirely numeric.")
        return super(RegisterPage, self).form_invalid(form)

        
    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        messages.success(self.request, f"Welcome to the resersi network!")
        messages.success(self.request, f"Count yourself lucky to join the community of the people that are going to change world.")
        messages.success(self.request, f"Create or take any quiz.")
        login(self.request, user)

        messages.error(self.request, 'Username or password does not exist')
        return super(RegisterPage, self).form_valid(form)


    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.success(self.request, f"{self.request.user.username}, you've already registered!")
            return redirect('quiz:quizzes')
        
        if self.request.session.get('ref_profile') is not None:
            profile_id = self.request.session.get('ref_profile')
        return super(RegisterPage, self).get(request, *args, **kwargs)


# add login required
@login_required(redirect_field_name='next', login_url='account_login')
def ProfilePage(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, "Login to continue")
        return redirect('login')


    profile = get_object_or_404(Profile, user=user)
    follower = Follower.objects.prefetch_related('followers','following').get(user=user)
    followersCount = follower.followers.all().count()
    followingsCount = follower.following.all().count()
    link = Link.objects.get(profile=profile)

    form = NewInterestReportForm()

    context={
        'profile': profile,
        'follower' : follower,
        'link':link,
        'nav': 'profile',
        'followersCount': followersCount,
        'followingsCount': followingsCount,
        'form' : form,
    }

    return render(request, 'core/profile.html', context)


@login_required(redirect_field_name='next', login_url='account_login')
def ProfileCreationPage(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(self.request, "Login to continue")
        return redirect('login')

    profile = get_object_or_404(Profile, user=user)

    form = ProfileCreationForm(instance=profile)
    print(form)

    if request.method == 'POST':
        form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}, you have successfully edited your profile.")
            messages.info(request, f"{user.username}, did you know that the brain neurons die one after the other if they are idle?")
            return redirect('profile')

    context = {
        'form': form,
    }

    return render(request, 'core/profile_form.html', context)





from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    template_name='core/change_password.html'

def password_success(request):
    return render(request, 'core/password_success.html', {})



@login_required(redirect_field_name='next', login_url='account_login')
def FollowerView(request):
    user = request.user
    if request.method == 'POST':
        following = request.POST.get('following') or None
        following_user = request.POST.get('following_user') or None
        following_username = request.POST.get('following_username') or None
        if user.id is not following:
            if following:
                following = Follower.objects.get(user=following)
                following_user = User.objects.get(username=following_user)#new
                follower = Follower.objects.get(user=user)#new
                following.followers.add(user)
                follower.following.add(following_user)#new
                following.save()
                follower.save()#new

        if user != following_user:
            return HttpResponse('follow')
            return redirect('profile:profile', profile_name=following_username)

    return redirect('profile')



@login_required(redirect_field_name='next', login_url='account_login')
def UnfollowView(request):
    user = request.user
    if request.method == 'POST':
        following = request.POST.get('following') or None
        following_user = request.POST.get('following_user') or None
        following_username = request.POST.get('following_username') or None
        if user.id is not following:
            if following:
                following = Follower.objects.get(user=following)
                following_user = User.objects.get(username=following_user)#new
                follower = Follower.objects.get(user=user)#new
                following.followers.remove(user)
                follower.following.remove(following_user)#new
                following.save()
                follower.save()#new

        if user != following_user:
            return HttpResponse('unfollow')

            return redirect('profile:profile', profile_name=following_username)

    return redirect('profile')





@login_required(redirect_field_name='next', login_url='account_login')
def EditLink(request):
    profile = Profile.objects.get(user=request.user)
    print(profile)
    link = Link.objects.get(profile=profile)
    print(link)
    
    form = NewLinkForm(instance=link)
    if request.method == 'POST':
        form = NewLinkForm(request.POST, instance=link)
        if form.is_valid():
            link.name = form.cleaned_data.get('name')
            link.link = form.cleaned_data.get('link')
            link.description = form.cleaned_data.get('description')
            link.save()
            return redirect('profile')

    context={
        'form': form,
    }

    return render(request, 'core/link.html', context)





def LinkClick(request, link_id):

    # link_id = request.GET.get('link_id')

    link = Link.objects.get(id=link_id)

    link.clicks += 1
    link.save()
    print(link.clicks)

    return HttpResponse('clicked')






def InterestReport(request):

    user = request.user
    print(user)
    if request.method == 'POST':
        print('The interest is received!')
        form = NewInterestReportForm(request.POST)
        if form.is_valid():
            interest = form.cleaned_data.get('interest')

            Interest.objects.create(user=user, interest=interest)
        return HttpResponse('report submitted!')




