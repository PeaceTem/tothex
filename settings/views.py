from inspect import classify_class_attrs
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views import View
from django.urls import reverse_lazy
from .forms import PasswordForm, ChangeUsernameForm
from django.contrib.auth import login, authenticate, update_session_auth_hash

from django.contrib.auth.models import User
from django.contrib import messages

from django.utils.translation import gettext_lazy as _



from django.http import HttpResponse, JsonResponse

from core.models import Profile
from category.models import Category, MyCategory
# Create your views here.

class Settings(LoginRequiredMixin, TemplateView):
    template_name='settings/settings.html'





class SetPassword(LoginRequiredMixin, FormView):
    form_class=PasswordForm
    template_name = 'settings/change_password.html'
    success_url = reverse_lazy('logout')


    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_password')
        confirm_new_password = form.cleaned_data.get('confirm_new_password')
        if new_password == confirm_new_password:
            user = self.request.user

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(self.request, user)
            
            messages.success(self.request, _("Password changed successfully"))
            # return redirect('auth:logout')
           
        else:
            messages.error(self.request, _("The new passwords don't match"))

            return redirect(self.request.META['HTTP_REFERER'])


        return super(SetPassword, self).form_valid(form)



class ChangeUsername(LoginRequiredMixin, FormView):
    template_name='settings/change_password.html'
    success_url=reverse_lazy('logout')
    form_class=ChangeUsernameForm


    def form_valid(self, form):
        new_username = form.cleaned_data.get('new_username')
        confirm_new_username = form.cleaned_data.get('confirm_new_username')

        if new_username == confirm_new_username:
            user = self.request.user
            # add username validator here
            user.username = new_username
            user.save()

        else:
            messages.error(self.request, _("The new usernames don't match"))
            return redirect(self.request.META['HTTP_REFERER'])
        return super(ChangeUsername, self).form_valid(form)


class EditProfileCategory(LoginRequiredMixin, View):
    # use detail view with profile here
    def get(self, request):
        user = self.request.user
        # profile = Profile.objects.prefetch_related('categories').get(user=user)
        categories = Category.objects.all().order_by('-quiz_number_of_times_taken')[:20]
        objCategories = user.myCategories.all()
        # print(objCategories)
        context={
            'user': user,
            # 'objCategories': profile.categories.all(),
            'objCategories': objCategories,
            'obj_type': 'profile',
            'page_obj': categories,
        }
        return render(self.request, 'quiz/categoryCreate.html', context)


"""
Remove the create ability from the form in category create using e.preventDefault
on submit
"""

class AddProfileCategory(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        data = self.request.GET.get('data')
        profile = Profile.objects.prefetch_related('categories').get(user=user)
        category_to_be_added = Category.objects.get(title=data)
        """
        I didn't use while loop because the newly added category might be the result of first()

        """
        if user.myCategories.count() > 9:
            user.myCategories.first().delete()

        MyCategory.objects.create(user=user, category=category_to_be_added)
        profile.categories.add(category_to_be_added)

        return JsonResponse({"categories":[x.title for x in profile.categories.all()],
                             "category_count": profile.categories.count(),})


        # return JsonResponse({"categories":[str(x) for x in user.myCategories.all()],
        #                      "category_count": user.myCategories.count(),})
     



class RemoveProfileCategory(LoginRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        profile = Profile.objects.prefetch_related('categories').get(user=user)
        data = self.request.GET.get('data')
        category_to_be_removed = Category.objects.get(title=data)
        """
        I didn't use while loop because the newly added category might be the result of first()

        """
        # if profile.categories.count() < 1:
        #     return
        # profile.categories.remove(category_to_be_removed)


        if user.myCategories.count() <= 1:
            print(user.myCategories.all())
            return HttpResponse('What The Fuck!')
        # user.myCategories.remove(category_to_be_removed)
        # user.myCategories.get(category=category_to_be_removed).delete()
        user.myCategories.filter(category=category_to_be_removed).delete()
        profile.categories.remove(category_to_be_removed)
        return JsonResponse({"categories":[x.title for x in profile.categories.all()],
                             "category_count": profile.categories.count(),})

        # return JsonResponse({"categories":[str(x) for x in user.myCategories.all()],
        #                      "category_count": user.myCategories.count(),})
     



