from django.shortcuts import render, redirect
from core.models import Profile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from .models import Q,A, Reply
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .forms import QuestionForm, AnswerForm, ReplyForm

from django.urls import reverse_lazy

from category.models import Category

from django.db.models import Q as Qlookup,F
from .serializers import QSerializer
from django.core.paginator import Paginator



class QuestionPage(TemplateView):
    template_name = 'q/question_page.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        search_input = self.request.GET.get('search-area') or ''
        context['search_input'] = search_input
        if user.is_authenticated:
            context['profile'] = Profile.objects.get(user=user)
        if search_input:
            context['page_obj'] = Q.objects.none()

            search = search_input.strip()
            search = search.split()
            for search_word in search:
                lookup = Qlookup(question__icontains=search_word) | Qlookup(description__icontains=search_word)
                context['page_obj'] |= Q.objects.filter(lookup)
        
        else:
            context['page_obj'] = Q.objects.all()
        context['form'] = QuestionForm
        context['nav'] = 'qxa'
        p = Paginator(context['page_obj'], 5)
        page = self.request.GET.get('page')
        context['page_obj'] = p.get_page(page)
        return context

        # add some postgres lookup here, like searchRank, searchQuery, etc.





class MyQPage(LoginRequiredMixin,TemplateView):
    redirect_field_name='next'
    template_name = 'q/question_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = user.profile
        search_input = self.request.GET.get('search-area') or ''
        context['search_input'] = search_input
        if search_input:
            context['page_obj'] = Q.objects.none()

            search = search_input.strip()
            search = search.split()
            for search_word in search:
                lookup = Qlookup(question__icontains=search_word) | Qlookup(description__icontains=search_word)
                context['page_obj'] |= context['profile'].questions.filter(lookup)


        else:
            context['page_obj'] = context['profile'].questions.all()
        p = Paginator(context['page_obj'], 5)
        page = self.request.GET.get('page')
        context['page_obj'] = p.get_page(page)
        context['nav'] = 'qxa'
        context['form'] = QuestionForm


        return context





class MyAPage(LoginRequiredMixin,TemplateView):
    redirect_field_name='next'
    template_name = 'q/question_page.html'
    # create another template for this
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = user.profile
        context['page_obj'] = context['profile'].answers.all()
        p = Paginator(context['page_obj'], 5)
        page = self.request.GET.get('page')
        context['page_obj'] = p.get_page(page)
        return context







class AnswerPage(DetailView):
    template_name = 'q/answer_page.html'
    model = Q
    context_object_name = 'q'
    # slug_field = 'slug'

    def get(self,request, slug, pk):
        return super(AnswerPage, self).get(request, slug, pk)



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'].views += 1
        context['q'].save()
        context['form'] = AnswerForm
        context["replyForm"]= ReplyForm	
        return context



class CreateQuestion(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    model = Q
    form_class = QuestionForm
    template_name = 'q/create_question.html'
    success_url = reverse_lazy('qxa:question-page')
    # add slug field to this view later.

    def post(self, request):
        form = QuestionForm(self.request.POST)
        if form.is_valid():
            user = self.request.user
            profile = Profile.objects.get(user=user)
            question = self.request.POST.get('question')
            description = self.request.POST.get('description')

            q = Q.objects.create(question=question, description=description, profile=profile)
            data = QSerializer(q).data
            # Add categories
            categories = self.request.POST.get('categories')
            if categories:
                for c in categories:
                    q.categories.add(c)
                    q.save()

            print(model_to_dict(q))
            print('The next one\n')
            print(data)
            return JsonResponse(data)
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

    def get(self, request, *args, **kwargs):
        return super(CreateQuestion, self).get(request)








class CreateAnswer(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    model = A
    form_class = AnswerForm
    template_name = 'q/create_question.html'
    success_url = reverse_lazy('qxa:question-page')

    def post(self, request, q_id):
        form = AnswerForm(self.request.POST)
        if form.is_valid():
            user = self.request.user
            profile = user.profile
            answer = self.request.POST.get('answer')
            question = Q.objects.get(id=q_id)
            A.objects.create(answer=answer, profile=profile, question=question)
            return HttpResponse('Answered!')
            return redirect('qxa:answer-page', slug=question.slug)
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

# Remove loginrequired mixin from every view here
class CreateReply(LoginRequiredMixin, CreateView):
	
	def post(self, request, a_id):
		user = self.request.user
		profile = user.profile
		answer = A.objects.get(id=a_id)
		reply = self.request.POST.get('reply')
		Reply.objects.create(profile=profile, answer=answer, reply=reply)
		return HttpResponse('Replied!')
        # return redirect('qxa:answer-page', slug=answer.question.slug)





# upvote and downvote section
class UpvoteQuestion(LoginRequiredMixin, View):
    def get(self, request, q_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        question = Q.objects.select_related('profile').prefetch_related('upvoters').get(id=q_id)
        upvoted_profile = question.profile
        if not profile in question.upvoters.all():
            question.upvoters.add(profile)
            upvoted_profile.coins += 1
            upvoted_profile.total_coins += 1
            upvoted_profile.save()
            return HttpResponse('upvoted!')
        else:
            question.upvoters.remove(profile)
            upvoted_profile.coins -= 1
            upvoted_profile.total_coins -= 1
            upvoted_profile.save()
            
            return HttpResponse('Not upvoted!')
        
        return HttpResponse('An error occurred!')





class DownvoteQuestion(LoginRequiredMixin, View):
    def get(self, request, q_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        question = Q.objects.select_related('profile').prefetch_related('downvoters').get(id=q_id)
        downvoted_profile = question.profile
        
        
        if not profile in question.downvoters.all():
            question.downvoters.add(profile)
            downvoted_profile.total_coins -= 1
            downvoted_profile.coins -= 1
            downvoted_profile.save()
            return HttpResponse('downvoted!')
        else:
            question.downvoters.remove(profile)
            downvoted_profile.total_coins += 1
            downvoted_profile.coins += 1
            downvoted_profile.save()

            return HttpResponse('Not downvoted!')

        return HttpResponse('An error occurred!')




class UpvoteAnswer(LoginRequiredMixin, View):
    def get(self, request, a_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        answer = A.objects.select_related('profile').prefetch_related('upvoters').get(id=a_id)
        upvoted_profile = answer.profile
        if not profile in answer.upvoters.all():
            answer.upvoters.add(profile)
            upvoted_profile.coins += 1
            upvoted_profile.total_coins += 1
            upvoted_profile.save()
            return HttpResponse('upvoted!')
        else:
            answer.upvoters.remove(profile)
            upvoted_profile.coins -= 1
            upvoted_profile.total_coins -= 1
            upvoted_profile.save()
            return HttpResponse('Not upvoted!')
        return HttpResponse('An error occurred!')





class DownvoteAnswer(LoginRequiredMixin, View):
    def get(self, request, q_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        answer= A.objects.select_related('profile').prefetch_related('downvoters').get(id=q_id)
        downvoted_profile = answer.profile
        if not profile in answer.downvoters.all():
            answer.downvoters.add(profile)
            downvoted_profile.total_coins -= 1
            downvoted_profile.coins -= 1
            downvoted_profile.save()
            return HttpResponse('downvoted!')
        else:
            answer.downvoters.remove(profile)
            downvoted_profile.total_coins += 1
            downvoted_profile.coins += 1
            downvoted_profile.save()
            return HttpResponse('Not downvoted!')
        return HttpResponse('An error occurred!')



from category.serializers import CategorySerializer
import json
# from rest_framework import generics
class CategoryList(View):
    def get(self, request):
        text = self.request.GET.get('text')
        categories = Category.objects.filter(title__icontains=text).values('title')
        print(categories)
        categories = CategorySerializer(categories).data
        print(categories)

        return JsonResponse(json.dumps(dict(categories)))



