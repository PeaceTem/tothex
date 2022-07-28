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



from .serializers import QSerializer




class QuestionPage(TemplateView):
    template_name = 'q/question_page.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = Profile.objects.get(user=user)
        context['qs'] = Q.objects.all()
        context['form'] = QuestionForm

        return context



class AnswerPage(DetailView):
    template_name = 'q/answer_page.html'
    model = Q
    context_object_name = 'q'
    slug_field = 'slug'


    def get_object(self):
        return self.model.objects.prefetch_related('answers').get(slug=self.kwargs['slug'])



    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = AnswerForm
        context["replyForm"]= ReplyForm	
        return context



class CreateQuestion(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    model = Q
    form_class = QuestionForm
    template_name = 'q/create_question.html'
    success_url = reverse_lazy('qxa:question-page')

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
            # for c in categories:
            #     q.categories.add(c)
            #     q.save()
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
            profile = Profile.objects.get(user=user)
            answer = self.request.POST.get('answer')
            question = Q.objects.get(id=q_id)
            A.objects.create(answer=answer, profile=profile, question=question)
            
            return redirect('qxa:answer-page', slug=question.slug)
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

# Remove loginrequired mixin from every view here
class CreateReply(LoginRequiredMixin, CreateView):
	
	def post(self, request, a_id):
		user = self.request.user
		profile = Profile.objects.get(user=user)
		answer = A.objects.select_related('question').get(id=a_id)
		reply = self.request.POST.get('reply')
		Reply.objects.create(profile=profile, answer=answer, reply=reply)
		return redirect('qxa:answer-page', slug=answer.question.slug)





# upvote and downvote section
class UpvoteQuestion(LoginRequiredMixin, View):
	def get(self, request, q_id):
		user = self.request.user
		profile = Profile.objects.get(user=user)
		question = Q.objects.prefetch_related('upvoters').get(id=q_id)
		if not profile in question.upvoters.all():
			question.upvoters.add(profile)

            # return HttpResponse('upvoted!')
		else:
			question.upvoters.remove(profile)
            # return HttpResponse('Not upvoted!')
		return HttpResponse('An error occurred!')





class DownvoteQuestion(LoginRequiredMixin, View):
	def get(self, request, q_id):
		user = self.request.user
		profile = Profile.objects.get(user=user)
		question = Q.objects.prefetch_related('downvoters').get(id=q_id)
		if not profile in question.downvoters.all():

			question.downvoters.add(profile)
            # return HttpResponse('downvoted!')
		else:
			question.downvoters.remove(profile)
            # return HttpResponse('Not downvoted!')
		return HttpResponse('An error occurred!')




class UpvoteAnswer(LoginRequiredMixin, View):
	def get(self, request, a_id):
		user = self.request.user
		profile = Profile.objects.get(user=user)
		answer = A.objects.prefetch_related('upvoters').get(id=q_id)
		if not profile in answer.upvoters.all():

			answer.upvoters.add(profile)
            # return HttpResponse('upvoted!')
		else:
			answer.upvoters.remove(profile)
            # return HttpResponse('Not upvoted!')
		return HttpResponse('An error occurred!')





class DownvoteAnswer(LoginRequiredMixin, View):
	def get(self, request, q_id):
		user = self.request.user
		profile = Profile.objects.get(user=user)
		answer= A.objects.prefetch_related('downvoters').get(id=q_id)
		if not profile in answer.downvoters.all():

			answer.downvoters.add(profile)
            # return HttpResponse('downvoted!')
		else:
			answer.downvoters.remove(profile)
            # return HttpResponse('Not downvoted!')
		return HttpResponse('An error occurred!')





class CategoryList(View):
	def get(self, request, text):
		categories = Category.objects.filter(title__icontains=text)
		# serialize this if it gives any error
		return JsonResponse(model_to_dict(categories))		
