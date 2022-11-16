from django.shortcuts import render, redirect
from category.services import removeFirstUserCategory
from core.models import Profile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.forms.models import model_to_dict
from .models import Q,A, Reply, SavedQuestion
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .forms import QuestionForm, AnswerForm, ReplyForm

from django.urls import reverse_lazy

from category.models import Category, MyCategory

from django.db.models import Q as Qlookup,F
from .serializers import QSerializer
from django.core.paginator import Paginator

from django.utils.text import slugify
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
"""
Change this page to listview
"""

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




"""
Change this page to listview too
"""
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



"""
Change this view to list view
"""

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






"""
Add the docs here
"""
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




"""
Add the docs here:
use form valid and form invalid for all create and form view
"""
class CreateQuestion(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    model = Q
    form_class = QuestionForm
    template_name = 'q/create_question.html'
    success_url = reverse_lazy('qxa:question-page')
    # add slug field to this view later.

    def post(self, request, *args, **kwargs):
        form = QuestionForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            user = self.request.user
            profile = Profile.objects.get(user=user)
            # question = self.request.POST.get('question')
            question = form.cleaned_data.get('question')
            # description = self.request.POST.get('description')
            description = form.cleaned_data.get('description')
            question_image = form.cleaned_data.get('question_image')

            q = Q.objects.create(
                question=question,
                description=description,
                profile=profile,
                question_image=question_image
                )
            # data = QSerializer(q).data
            # Add categories

            # categories = self.request.POST.get('categories')
            # if categories:
            #     for c in categories:
            #         q.categories.add(c)
            #         q.save()

            # print(model_to_dict(q))
            # print('The next one\n')
            # print(data)
            # return JsonResponse(data)
            return redirect('qxa:category-create', q.id)
        messages.error(self.request, _("An Error Occurred!"))
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

    def get(self, request, *args, **kwargs):
        return super(CreateQuestion, self).get(request)









"""
Add the docs here
"""
class CreateAnswer(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    model = A
    form_class = AnswerForm
    template_name = 'q/create_question.html'
    success_url = reverse_lazy('qxa:question-page')

    def post(self, request, q_id):
        form = AnswerForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            user = self.request.user
            profile = user.profile
            answer = form.cleaned_data.get('answer')
            solution_image = form.cleaned_data.get('solution_image')
            question = Q.objects.get(id=q_id)
            A.objects.create(
                answer=answer,
                solution_image=solution_image,
                profile=profile,
                question=question
                )
            messages.success(self.request, _("Answer submitted!"))
            # return HttpResponse('Answered!')
            # return redirect('qxa:answer-page', slug=question.slug)
        return HttpResponseRedirect(self.request.META['HTTP_REFERER'])


"""
Add the docs here
"""
# Remove loginrequired mixin from every view here
class CreateReply(LoginRequiredMixin, CreateView):
	
	def post(self, request, a_id):
		user = self.request.user
		profile = user.profile
		answer = A.objects.get(id=a_id)
		reply = self.request.POST.get('reply')
		Reply.objects.create(
            profile=profile,
            answer=answer,
            reply=reply
            )
		return HttpResponse('Replied!')
        # return redirect('qxa:answer-page', slug=answer.question.slug)






"""
Add the docs here
"""
# upvote and downvote section
class UpvoteQuestion(LoginRequiredMixin, View):
    def get(self, request, q_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        question = Q.objects.select_related('profile').prefetch_related('upvoters', 'downvoters').get(id=q_id)
        upvoted_profile = question.profile
        # check if the upvoter is not the creator of the question

        # if profile == question.profile:
        #     return HttpResponseForbidden()

        if not profile in question.upvoters.all():
            question.upvoters.add(profile)
            if profile in question.downvoters.all():
                question.downvoters.remove(profile)
            upvoted_profile.coins += 1
            upvoted_profile.total_coins += 1
            upvoted_profile.save()
            return JsonResponse({"upvote_count": question.upvoters.count(),"downvote_count":question.downvoters.count(), "action":"upvote"})
            # return HttpResponse('upvoted!')
        else:
            question.upvoters.remove(profile)
            upvoted_profile.coins -= 1
            upvoted_profile.total_coins -= 1
            upvoted_profile.save()
            return JsonResponse({"upvote_count": question.upvoters.count(), "downvote_count":question.downvoters.count(), "action":"remove upvote"})
            
            # return HttpResponse('Not upvoted!')
        
        # return HttpResponse('An error occurred!')






"""
Add the docs here
"""
class DownvoteQuestion(LoginRequiredMixin, View):
    def get(self, request, q_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        question = Q.objects.select_related('profile').prefetch_related('upvoters', 'downvoters').get(id=q_id)
        downvoted_profile = question.profile

        # if profile == question.profile:
        #     return HttpResponseForbidden()

        if not profile in question.downvoters.all():
            question.downvoters.add(profile)
            if profile in question.upvoters.all():
                question.upvoters.remove(profile)
            #remove the user from the upvoted
            #and do so for the upvote too. Remove user from the downvote
            downvoted_profile.total_coins -= 1
            downvoted_profile.coins -= 1
            downvoted_profile.save()
            return JsonResponse({"downvote_count": question.downvoters.count(),"upvote_count": question.upvoters.count(), "action":"downvote"})
            # return HttpResponse('downvoted!')
        else:
            question.downvoters.remove(profile)
            downvoted_profile.total_coins += 1
            downvoted_profile.coins += 1
            downvoted_profile.save()
            return JsonResponse({"downvote_count": question.downvoters.count(),"upvote_count": question.upvoters.count(), "action":"downvote"})

            # return JsonResponse({"count": question.downvoters.count(), "action":"downvote"})

            # return HttpResponse('Not downvoted!')

        # return HttpResponse('An error occurred!')





"""
Add the docs here
"""
class UpvoteAnswer(LoginRequiredMixin, View):
    def get(self, request, a_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        answer = A.objects.select_related('profile').prefetch_related('upvoters', 'downvoters').get(id=a_id)
        upvoted_profile = answer.profile

        # if profile == answer.profile:
        #     return HttpResponseForbidden()
            
        if not profile in answer.upvoters.all():
            answer.upvoters.add(profile)
            if profile in answer.downvoters.all():
                answer.downvoters.remove(profile)
            upvoted_profile.coins += 1
            upvoted_profile.total_coins += 1
            upvoted_profile.save()
            # return JsonResponse({"upvote_count": answer.upvoters.count(),"downvote_count":answer.downvoters.count(), "action":"upvote"})

            # return JsonResponse({"count": answer.upvoters.count(), "action":"upvote"})

            # return HttpResponse('upvoted!')
        else:
            answer.upvoters.remove(profile)
            upvoted_profile.coins -= 1
            upvoted_profile.total_coins -= 1
            upvoted_profile.save()
        return JsonResponse({"upvote_count": answer.upvoters.count(),"downvote_count":answer.downvoters.count(), "action":"upvote"})

            # return JsonResponse({"count": answer.upvoters.count(), "action":"downvote"})

            # return HttpResponse('Not upvoted!')
        # return HttpResponse('An error occurred!')






"""
Add the docs here
"""



class DownvoteAnswer(LoginRequiredMixin, View):
    def get(self, request, a_id):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        answer= A.objects.select_related('profile').prefetch_related('upvoters', 'downvoters').get(id=a_id)
        downvoted_profile = answer.profile

        # if profile == answer.profile:
        #     return HttpResponseForbidden()
            
        if not profile in answer.downvoters.all():
            answer.downvoters.add(profile)
            if profile in answer.upvoters.all():
                answer.upvoters.remove(profile)
            downvoted_profile.total_coins -= 1
            downvoted_profile.coins -= 1
            downvoted_profile.save()
            # return JsonResponse({"upvote_count": answer.upvoters.count(),"downvote_count":answer.downvoters.count(), "action":"upvote"})

            # return JsonResponse({"count": answer.downvoters.count(), "action":"downvote"})

            # return HttpResponse('downvoted!')
        else:
            answer.downvoters.remove(profile)
            downvoted_profile.total_coins += 1
            downvoted_profile.coins += 1
            downvoted_profile.save()
        return JsonResponse({"upvote_count": answer.upvoters.count(),"downvote_count":answer.downvoters.count(), "action":"upvote"})

            # return JsonResponse({"count": answer.downvoters.count(), "action":"downvote"})

            # return HttpResponse('Not downvoted!')
        # return HttpResponse('An error occurred!')



from category.serializers import CategorySerializer
import json
# from rest_framework import generics
class CategoryList(View):
    def get(self, request):
        text = self.request.GET.get('text')
        categories = Category.objects.filter(title__icontains=text).values('title')
        # print(categories)
        categories = CategorySerializer(categories).data
        # print(categories)

        return JsonResponse(json.dumps(dict(categories)))







"""
Add all the documentation here
"""

class CategoryCreate(LoginRequiredMixin, View):
    def get(self, request, q_id):
        user = request.user
        profile = Profile.objects.prefetch_related("categories").get(user=user)
        q = Q.objects.prefetch_related("categories").get(id=q_id)
        #make this part more efficient
        title = request.GET.get('newCategory') or ''
        title = slugify(title)
        if title:

            if q.categories.count() < 3:
                category = None
                try:
                    category = Category.objects.get(title__iexact=title)
                    if not category in q.categories.all():

                        q.categories.add(category)
                    else:
                        messages.warning(request, _(f"{category.title} has already been added to the question!"))
                except:
                    pass

                if not category:
                    newCategory = Category.objects.create(
                        registered_by=user,
                        title=title
                        )
                    q.categories.add(newCategory)
                    removeFirstUserCategory(user, profile)
                    # if user.myCategories.count() > 9:
                        # user.myCategories.first.delete()
                    MyCategory.objects.create(user=user, category=newCategory)
                    # if profile.categories.count() > 9:
                    #     removed = profile.categories.first()
                    #     profile.categories.remove(removed)
                    profile.categories.add(newCategory)

                    messages.success(request, _(f"{newCategory} has been added!"))



        addedCategory = request.GET.get("addedCategory") or ''
        if addedCategory:
            try:
                category = Category.objects.get(title__iexact=addedCategory) or None
                if category:
                    while q.categories.count() > 2:
                        removed = q.categories.first()
                        q.categories.remove(removed)
                    q.categories.add(category)

                    removeFirstUserCategory(user, profile)
                    # if user.myCategories.count() > 9:
                        # user.myCategories.first.delete()
                    MyCategory.objects.create(user=user, category=newCategory)

                    # while profile.categories.count() > 9:
                    #     removed = profile.categories.first()
                    #     profile.categories.remove(removed)
                    profile.categories.add(category)
            except:
                pass



        quizCategories = q.categories.all()
        if request.GET.get('request_type') == 'ajax':
            # just use this place to return the json response
            # print("Python just comes at you like motherfucker!")
            return JsonResponse({"categories":[x.title for x in quizCategories],
                                "category_count": q.categories.count(),})


        context= {
            # 'page_obj': user.myCategories.all(),
            'page_obj': profile.categories.all(),# use profile categories here
            'objCategories' : quizCategories,
            'q': q,
            'obj_type': 'qxa',
        }

        return render(request, 'quiz/categoryCreate.html', context)




"""
Add the docs here
"""
class CategoryRemove(LoginRequiredMixin, View):
    def get(self, request, q_id):
        q = Q.objects.prefetch_related('categories').get(id=q_id)
        category = request.GET.get('removedCategory')
        category = Category.objects.get(title=category)
        q.categories.remove(category)
        print('category removed')
        return JsonResponse({"categories":[x.title for x in q.categories.all()],
                            "category_count": q.categories.count(),})










class SaveQuestion(LoginRequiredMixin, View):
    def get(self, request, q_id):
        q = Q.objects.get(id=q_id)
        user = self.request.user
        SavedQuestion.objects.create(
            user=user,
            question=q
        )

        return HttpResponse




class RemoveSavedQuestion(LoginRequiredMixin, View):
    def get(self, request, save_question_id):
        saved_question = SavedQuestion.objects.select_related('user').get(id=save_question_id)
        user = self.request.user
        if user == saved_question.user:
            saved_question.delete()

        return HttpResponse


