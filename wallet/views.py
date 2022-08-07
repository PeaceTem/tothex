from locale import currency
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.base import TemplateView
from .models import Wallet, History
from core.models import Profile
# Create your views here.

class AcceptPayment(LoginRequiredMixin, View):
    def post(self, request):
        user = self.request.user
        profile = Profile.objecs.get(user=user)
        currency = self.request.POST.get('currency')

        amount = self.request.POST.get('amount')

        return redirect()


class SuccessPage(LoginRequiredMixin, TemplateView):
    template_name = ''