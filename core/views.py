from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse

# function based views
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User
from django.contrib import messages

from .models import Profile, Follower, Link, FeedBack
from .forms import FeedBackForm, ProfileCreationForm, LoginForm, NewLinkForm, ImageForm

from django.utils.translation import gettext_lazy as _

# services

from .services import ReferralService, get_user_ip
# # Create your views here.
# messages.error, warning, success, info, debug
 

# from importlib import import_module
# from django.conf import settings
# SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

def Menu(request):
    return render(request, 'menu.html')

def Home(request):
    return render(request, 'core/home.html', {})


def PrivacyPolicy(request):
    return render(request, 'privacy_policy.html')

def TermsAndConditions(request):
    return render(request, 'terms_and_conditions.html')


def Donate(request):
    return HttpResponseRedirect('https://paystack.com/pay/neugott-donation-for-the-developer')


def Chart(request):
    return render(request, 'core/chart.html')


class FeedBack(FormView):
    form_class = FeedBackForm
    template_name = 'core/feedback.html'
    model = FeedBack
    success_url = reverse_lazy('quiz:quizzes')

    def form_valid(self, form):
        feedback = form.save()
        feedback.user = self.request.user
        feedback.save()
        messages.success(self.request, _('Your feedback has been submitted!'))

        return super().form_valid(form)

class MyStruggle(TemplateView):
    template_name='core/my_struggle.html'


class Advertise(TemplateView):
    template_name='core/contact.html'

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
        ReferralService(request, code)
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


    profile = Profile.objects.select_related("user","streak").get(user=user)
    follower = Follower.objects.prefetch_related('followers','following').get(user=user)
    followersCount = follower.followers.all().count()
    # followingsCount = follower.following.all().count()
    followingsCount = user.followers.count()
    link = Link.objects.get(profile=profile)


    context={
        'user': user,
        'profile': profile,
        'follower' : follower,
        'link':link,
        'nav': 'profile',
        'followersCount': followersCount,
        'followingsCount': followingsCount,
    }

    return render(request, 'core/profile.html', context)


@login_required(redirect_field_name='next', login_url='account_login')
def ProfileCreationPage(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, "Login to continue")
        return redirect('login')

    profile = Profile.objects.get(user=user)

    form = ProfileCreationForm(instance=profile)

    if request.method == 'POST':
        form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.username}, you have successfully edited your profile.")
            return redirect('profile')

    context = {
        'form': form,
    }

    return render(request, 'core/profile_form.html', context)



# class EditProfilePicture(LoginRequiredMixin, FormView):
#     form_class = ImageForm
#     template_name = 'core/edit_profile_picture.html'
#     model = Profile
#     success_url = 'profile'

#     def form_valid(self,form):
#         form.save()
#         return super(EditProfilePicture, self).form_valid(form)

#     def get(self, request, profile_id):
#         profile = Profile.objects.get(id=profile_id)

class EditProfilePicture(LoginRequiredMixin, View):
    def get(self, request, profile_id):
        print('o de be!')
        profile = Profile.objects.get(id=profile_id)
        form = ImageForm(request.POST or None, request.FILES or None, instance=profile)
        # form = ImageForm(request.GET or None, request.FILES or None, instance=profile)

        context = {'form': form}
        return render(request, 'core/edit_profile_picture.html', context)

    def post(self, request, profile_id):
        print('Post is reached!')
        profile = Profile.objects.get(id=profile_id)
        form = ImageForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            print('Saved')
            form.save()
            return JsonResponse({'message': 'works'})
        return HttpResponse('Error')

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
def FollowView(request):
    user = request.user
    if request.method == 'POST':
        following = request.POST.get('following') or None
        following_user = request.POST.get('following_user') or None
        following_username = request.POST.get('following_username') or None
        if user is not following:
            if following:
                # following = Follower.objects.prefetch_related("followers").get(user=following)
                following = Follower.objects.prefetch_related("followers").get(id=following)
                print('Working', following)
                following_user = User.objects.get(username=following_user)#new
                print(following_user, 'that is following')
                follower = Follower.objects.prefetch_related("following").get(user=user)#new
                print(follower, 'the followee')
                following.followers.add(user)
                follower.following.add(following_user)#new
                # following.save()
                # follower.save()#new

        if user != following_user:
            return HttpResponse('follow')
            return redirect('profile:profile', profile_name=following_username)

    return redirect('profile')



@login_required(redirect_field_name='next', login_url='account_login')
def UnfollowView(request):
    user = request.user
    if request.method == 'POST':
        following = request.POST.get('following') or None
        print('following', following)
        following_user = request.POST.get('following_user') or None
        print('following_user', following_user)

        following_username = request.POST.get('following_username') or None
        print('following_username', following_username)
        if user is not following:
            if following:
                following = Follower.objects.prefetch_related("followers").get(user__username=following)
                # following_user = User.objects.get(username=following_user)#new
                follower = Follower.objects.prefetch_related('following').get(user=user)#new
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
    link = Link.objects.get(profile=profile)
    
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

    return HttpResponse('clicked')



# @login_required(redirect_field_name='next', login_url='account_login')
def FollowerListView(request, follower_id, page_name):
    search_input = request.GET.get('search-area') or ''
    if search_input:
        search_input = search_input.split()
        search_input = "_".join(search_input)
        searched_user = None
        try:
            searched_user = User.objects.get(username__iexact=search_input) or None
        except:
            pass
        if searched_user:
            # profile = Profile.objects.get(user=searched_user)
            return redirect('profile:profile', profile_name=searched_user)
        else:
            messages.error(request, f"There is no user named {search_input}")
            return redirect(request.META["HTTP_REFERER"])

    owner = None
    owner_followers = None
    if page_name == 'followers':
        follower = Follower.objects.select_related('user').prefetch_related('followers', 'following').get(id=follower_id)
        owner = follower.user
        owner_followers = owner.followers.all()
        object_type = 'followers'
    elif page_name == 'following':
        follower = Follower.objects.select_related('user').prefetch_related('following').get(id=follower_id)
        owner = follower.user
        follower = owner.followers.all()
        print(follower)
        # This place is not optimized and check other followers views

        object_type = 'following'

    else:
        return HttpResponse('Error!')

    context = {
        'objects' : follower,
        'object_type' : object_type,
        'follower_id': follower_id,
        'user': request.user,
        'owner': owner,
        'owner_followers': owner_followers,
    }

    return render(request, 'core/followerList.html', context)



    
# @login_required(redirect_field_name='next', login_url='account_login')
# def FollowActionView(request, follower_id, user_id, action):
#     user = request.user
#     follower = Follower.objects.select_related('user').prefetch_related('followers').get(id=follower_id) #the action taker

#     if not user == follower.user:

#         return HttpResponse('An Error Occurred!')
#     _user = User.objects.get(id=user_id)
#     _follower = Follower.objects.prefetch_related('followers').get(user=_user) # the action recipient
#     # Make some necessary adjustments here!

#     if action == 'follow':
#         follower.following.add(_user)
#         _follower.followers.add(user)
#         # follower.save()
#         # _follower.save()

#     elif action == 'unfollow':
#         follower.following.remove(_user)
#         _follower.followers.remove(user)
#         # follower.save()
#         # _follower.save()

#     return HttpResponse('Done!')

    



"""
The follower_id is for the leader
The user_id is for the followee
"""
@login_required(redirect_field_name='next', login_url='account_login')
def FollowActionView(request, follower_id, user_id, action):
    user = request.user
    follower = Follower.objects.select_related('user').get(id=follower_id) #the action taker
    print('user', user)
    print()
    print('follower', follower)
    print()
    if not user == follower.user:
        return HttpResponse('An Error Occurred!')
    _user = User.objects.get(id=user_id)
    _follower = Follower.objects.prefetch_related('followers','following').get(user=_user) # the action recipient
    # Make some necessary adjustments here!
    print('_user', _user)
    print()
    print('_follower', _follower)
    if action == 'follow':
        # follower.following.add(_user)
        _follower.followers.add(user)
        print('added')

    elif action == 'unfollow':
        # follower.following.remove(_user)
        _follower.followers.remove(user)
        print('removed')

    return HttpResponse('Done!')






def allow_notification(request):
    user = request.user
    if user.is_authenticated:
        profile = user.profile
        profile.coins += 40
        profile.save()
    return HttpResponse("40 coins added!")






