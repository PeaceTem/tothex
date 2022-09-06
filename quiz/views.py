# django 
# important method to deal with models
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.db.models import Q, Avg, Min, Max, F, Count, Sum
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# all the forms
# the forms for each model
from .forms import NewQuizForm, NewFourChoicesQuestionForm, NewTrueOrFalseQuestionForm, NewQuizLinkForm
from category.forms import NewCategoryForm
# all the models
# the models to be used to create the quiz app

from django.contrib.auth.models import User
from core.models import Follower
from category.models import Category
from .models import Quiz, QuizLink, Attempter
from question.models import TrueOrFalseQuestion, FourChoicesQuestion
from core.models import Streak, Profile
from ads.models import PostAd


# celery tasks
from core.tasks import LikeQuiz, StreakValidator, CoinsTransaction, CreatorCoins


# services

from core.services import ReferralService, get_user_ip
from .services import ScoreRange, generateCoins
from ads.services import getAd
# Utilities
import random
from random import shuffle
from .utils import render_to_pdf, sortKey, quizRandomCoin, randomChoice, sortQuiz

import decimal


from django.utils.text import slugify

def CustomCheckbox(request):
    return render(request, 'quiz/custom-checkbox.html')


"""
Create a page for only users that are not logged in to taste the fun of the app before signing up
"""

class GeneratePDF(LoginRequiredMixin, View):

    def get(self, request, quiz_id, **kwargs):
        # user = self.request.user
        number_of_registered_users = Profile.objects.all().count()
        template = get_template('quiz/takequiz.html')
        quiz = Quiz.objects.prefetch_related('fourChoicesQuestions', 'trueOrFalseQuestions').get(id=quiz_id)

        preQuestions = []
        preQuestions += quiz.fourChoicesQuestions.all()
        preQuestions += quiz.trueOrFalseQuestions.all()
        questionsList = []
        for question in preQuestions:
            questionsList.append(tuple((question.index, question)))


        questionsList.sort(key=sortKey)
        questions = []
        for question in questionsList:
            questions.append(question[1])
        if request.method == 'GET':
            if quiz.shuffleQuestions:
                shuffle(questions)

        context = {
            'quiz': quiz,
            'questions': questions,
            'number_of_registered_users': number_of_registered_users,
        }

        pdf = render_to_pdf('quiz/quizPdf.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"NeuGott_quiz_{quiz.title}.pdf"
            # content = f"inline; filename={filename}"
            content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content

            return response
        return HttpResponse("Not Found!")



# the details of a quiz

def QuizDetail(request, quiz_id, quiz_slug, *args, **kwargs):
    try:
        user = request.user
        quiz = Quiz.objects.select_related("quizlink").prefetch_related("likes", "categories").get(id=quiz_id)
        quiz.views += 1
        quiz.save()
        preQuestions = []
        preQuestions += quiz.fourChoicesQuestions.all()
        preQuestions += quiz.trueOrFalseQuestions.all()
        questions = []
        for question in preQuestions:
            questions.append(tuple((question.index, question)))


        questions.sort(key=sortKey)
        profile = None
        number_of_registered_users = Profile.objects.all().count()
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
        if not user.is_authenticated:
            code = str(kwargs.get('ref_code'))
            ReferralService(request, code)
        
        # postAd = PostAd.objects.all()
        # if postAd.count() > 0:
        #     postAd = randomChoice(postAd)
        #     postAd.views += 1
        #     postAd.detailpageviews += 1
        #     postAd.save()
    except:
        return redirect('quiz:my-quizzes')    
    context = {
        'quiz': quiz,
        'user': user,
        'postAd': getAd('detail'),
        'page' : 'detail',
        'profile': profile or 'None',
        'number_of_registered_users': number_of_registered_users,
        'questions': questions,
    }

    try:
        if quiz.quizlink.name and quiz.quizlink.link and quiz.quizlink.description:

            context['quizLink'] = quiz.quizlink
    except:
        pass

    
    try:
        attempters = quiz.attempters.all()[:10]
        context['attempters'] = attempters
    except:
        pass


    return render(request, 'quiz/quizdetail.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def CreateObject(request):
    return render(request, 'quiz/create.html')


"""
Add all the documentation here
"""
# the quiz list view
# @login_required(redirect_field_name='next', login_url='account_login')
def QuizList(request):
    user = request.user
    profile = None
    page_count = 5
    page = request.GET.get('page') or 1
    

    search_input= request.GET.get('search-area') or ''
    if search_input:
        quizzes = Quiz.objects.none()
        search = search_input.strip()
        search = search.split()
        page_count = 20
        for search_word in search:

            lookup = Q(title__icontains=search_word) | Q(description__icontains=search_word) | Q(categories__title__icontains=search_word) | Q(user__username__icontains=search_word)
            quizzes |= Quiz.objects.filter(lookup).order_by("-relevance")
        
        quizzes = quizzes.order_by('-relevance').distinct()[:100]
    else:
        if user.is_authenticated:
            profile = Profile.objects.prefetch_related( 'recommended_quizzes', 'categories', 'quizTaken').get(user=user)
            if profile.recommended_quizzes.count() < page_count:
                categories = profile.categories.all()
                age = profile.get_user_age
                lookup = Q(age_from__lte=age) & Q(age_to__gte=age) #& Q(questionLength__gte=3)
                while categories.count() > 0 and profile.recommended_quizzes.count() <= 300:
                # use while loop to check for quiz length
                    category = randomChoice(categories)
                    categories = categories.exclude(id=category.id)
                    quizzes = category.quizzes.filter(lookup)[:150]
                    for q in quizzes:
                        if q not in profile.quizTaken.all():
                            profile.recommended_quizzes.add(q)


            if profile.recommended_quizzes.count() > 0:
                page = 1
                page_count = 5
                quizzes = profile.recommended_quizzes.all()[:page_count + 1]
                for rem in quizzes:
                    profile.recommended_quizzes.remove(rem)



        else:
            lookup = Q(relevance__gte=0) & Q(questionLength__gte=0)
            quizzes = Quiz.objects.filter(lookup).order_by('?')[:100]

    p = Paginator(quizzes, page_count)
    quizzes = p.get_page(page)


    context={

        'search_input': search_input,
        'page_obj': quizzes,
        'profile': profile,
        'nav': 'quizzes',
    }


    return render(request, 'quiz/quizzes_list.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def FollowerQuizList(request):
    user = request.user
    follow = Follower.objects.get(user=user)
    profile = Profile.objects.prefetch_related('quizTaken').get(user=user)
    quizzes = Quiz.objects.none()
    # add more abstraction for efficiency
    for following in follow.following.all():
        quizzes |= Quiz.objects.filter(user=following)
    quizzes = quizzes.distinct()

    search_input= request.GET.get('search-area') or ''
    if search_input:
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup = Q(user=search_word) | Q(user__username__icontains=search_word) | Q(title__icontains=search_word) | Q(description__icontains=search_word)
            quizzes = quizzes.filter(lookup).distinct()
    else:

        takenQuiz = profile.quizTaken.all()

        randomQuizzes = []
        while len(randomQuizzes) < 100 and quizzes.count() > 0:
            quiz = randomChoice(quizzes)
            # print(quiz)
            quizzes = quizzes.exclude(id=quiz.id)
            if quiz not in takenQuiz:
                randomQuizzes.append(quiz)
            
        quizzes = randomQuizzes
        

    # create pagination
    p = Paginator(quizzes, 10)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context={
        'page_obj': quizzes,
        'nav': 'following-quizzes',
        'profile': profile,
    }


    return render(request, 'quiz/quizzes_list.html', context)





@login_required(redirect_field_name='next', login_url='account_login')
def MyQuizList(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    quizzes = user.quiz_set.all()

    search_input= request.GET.get('search-area') or ''
    if search_input:
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup = Q(title__icontains=search_word) | Q(description__icontains=search_word)
            quizzes = quizzes.filter(lookup).distinct()

    # create pagination
    p = Paginator(quizzes, 10)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context={
        'page_obj': quizzes,
        'nav': 'my-quizzes',
        'profile': profile,
    }


    return render(request, 'quiz/quizzes_list.html', context)



def VisitorView(request, owner_id):
    user = User.objects.get(id=owner_id)
    profile = Profile.objects.get(user=user)
    quizzes = user.quiz_set.all()


    search_input= request.GET.get('search-area') or ''
    if search_input:
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup = Q(title__icontains=search_word) | Q(description__icontains=search_word)
            quizzes = quizzes.filter(lookup).distinct()

    # create pagination
    p = Paginator(quizzes, 10)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context={
        'page_obj': quizzes,
        'nav': 'my-quizzes',
        'profile': profile,
    }


    return render(request, 'quiz/quizzes_list.html', context)








@login_required(redirect_field_name='next', login_url='account_login')
def QuizTakenList(request):
    user = request.user
    profile = Profile.objects.prefetch_related('quizTaken').get(user=user)
    quizzes = profile.quizTaken.all()

    search_input= request.GET.get('search-area') or ''
    if search_input:
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup = Q(title__icontains=search_word) | Q(description__icontains=search_word)
            quizzes = quizzes.filter(lookup).distinct()

    # create pagination
    p = Paginator(quizzes, 10)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context={
        'page_obj': quizzes,
        'nav': 'quizTaken',
        'profile': profile,
    }


    return render(request, 'quiz/quizzes_list.html', context)





@login_required(redirect_field_name='next', login_url='account_login')
def FavoriteQuizList(request):
    user = request.user
    profile = Profile.objects.prefetch_related('favoriteQuizzes').get(user=user)
    quizzes = profile.favoriteQuizzes.all()
    search_input= request.GET.get('search-area') or ''
    if search_input:
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup = Q(title__icontains=search_word) | Q(description__icontains=search_word)
            quizzes = quizzes.filter(lookup).distinct()
        


    p = Paginator(quizzes, 10)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context={
        'page_obj': quizzes,
        'nav': 'favorites',
        'profile': profile,
    }
    return render(request, 'quiz/quizzes_list.html', context)








@login_required(redirect_field_name='next', login_url='account_login')
def CategoryQuizList(request, category):
    quizzes = Quiz.objects.filter(categories__title=category, relevance__gte=51).order_by("solution_quality")[:100]
    user = request.user
    category = Category.objects.get(title=category)
    quizzes = category.quizzes.filter(relevance__gte=51).order_by('solution_quality')[:100]
    profile = Profile.objects.get(user=user)

    search_input= request.GET.get('search-area') or ''
    if search_input:
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup = Q(title__icontains=search_word) | Q(description__icontains=search_word)
            quizzes = quizzes.filter(lookup).distinct()
        


    p = Paginator(quizzes, 20)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context={
        'page_obj': quizzes,
        'nav': 'my-quizzes',
        'profile': profile,
    }

    return render(request, 'quiz/quizzes_list.html', context)




"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def PostLike(request):
    user = request.user
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')
        quiz = Quiz.objects.prefetch_related('likes').select_related('user').get(id=quiz_id)
        profile = Profile.objects.get(user=quiz.user)
        likeProfile = Profile.objects.prefetch_related('favoriteQuizzes').select_related('favoriteUser').get(user=user)


        if user in quiz.likes.all():
            quiz.likes.remove(user)
            quiz.likeCount -= 1
            profile.likes -= 1
            likeProfile.favoriteQuizzes.remove(quiz)
            likeProfile.save()
            quiz.save()
            profile.save()

            # following.save()
            # follower.save()
            return HttpResponse('unliked')

        else:
            quiz.likes.add(user)
            profile.likes += 1
            quiz.likeCount += 1
            likeProfile.favoriteQuizzes.add(quiz)
            likeProfile.favoriteUser = user
            quiz.save()
            profile.save()
            likeProfile.save()
            following = Follower.objects.prefetch_related("followers").get(user=quiz.user)
            # following_user = User.objects.get(username=following_user)
            follower = Follower.objects.prefetch_related("following").get(user=user)
            if user not in following.followers.all():
                following.followers.add(user)
                follower.following.add(quiz.user)
            return HttpResponse('liked')


        """
        This is a celery command
        Remove this from the celery tasks
        """

        # LikeQuiz.delay(quiz_id, user)


    return HttpResponse('Error!')

# make this function available to every one
class RandomQuizPicker(View):
    def get(self, request):
        # print(self.request.META["HTTP_USER_AGENT"])
        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.prefetch_related("categories").get(user=user)
            categories = profile.categories.all()
            quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=5, solution_quality__gt=3, average_score__gte=50).distinct()[:100]
            quiz = None
            if not quizzes.count() > 0:
                quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=5, solution_quality__gt=0).distinct()[:100]

            
            if not quizzes.count() > 0:
                quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=5)[:100]
        else:
            quizzes = Quiz.objects.filter(questionLength__gte=0)

        if quizzes.count() > 0:
            quiz = randomChoice(quizzes)

            if not quiz:
                messages.error(self.request, _('There is no quiz available'))
                return redirect('quiz:quizzes')
            return redirect('quiz:take-quiz', quiz_id=quiz.id)
        return HttpResponse("An error Occurred!")
        # return redirect('quiz:take-quiz', quiz_id=quiz.id)






"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def QuizCreate(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = NewQuizForm()
    if request.method == 'POST':
        form = NewQuizForm(request.POST)
        if form.is_valid():
            title= form.cleaned_data.get('title')
            description=form.cleaned_data.get('description')
            shuffleQuestions = form.cleaned_data.get('shuffleQuestions')
            age_from = form.cleaned_data.get('age_from')
            age_to = form.cleaned_data.get('age_to')
            quiz = Quiz.objects.create(user=user, title=title, description=description, shuffleQuestions=shuffleQuestions, age_from=age_from, age_to=age_to)
            profile.quizzes += 1
            profile.save()
            return redirect('quiz:create-quiz-link', quiz_id=quiz.id)
    
    context= {
        'form': form,
    }

    return render(request, 'quiz/quizCreate.html', context)



# use create view later
class QuizLinkCreate(LoginRequiredMixin, View):

    def get(self, request, quiz_id, *args, **kwargs):
        quiz = Quiz.objects.select_related('quizlink', 'user').get(id=quiz_id)
        try:
            if quiz.quizlink.link:
                return redirect('quiz:category-create', quiz_id=quiz.id)
        except:
            pass
        form = NewQuizLinkForm()
        context = {
            'form': form,
            'quiz': quiz,
        }
        return render(request, 'quiz/quizzes_form.html', context)
     

    def post(self, request, quiz_id, *args, **kwargs):
        try:
            form = NewQuizLinkForm(self.request.POST)
            if form.is_valid():
                user = self.request.user
                quiz = Quiz.objects.get(id=quiz_id)


                if user != quiz.user:
                    messages.error(self.request, _('You are not authorize to add a link'))
                    return redirect('quiz:quizzes')
                try:
                    if quiz.quizlink:
                        messages.warning(self.request, _('You have already added a link to this quiz!'))
                        return redirect('quiz:category-create', quiz_id=quiz.id)
                except:
                    pass
                name = self.request.POST.get('name')
                link = self.request.POST.get('link')
                description = self.request.POST.get('description')
                quizLink = QuizLink.objects.create(quiz=quiz, name=name, link=link, description=description)
                return redirect('quiz:category-create', quiz_id=quiz.id)
        except:
            # add IntegrityError 
            messages.error(self.request, _('An error occurred!'))
            return redirect('quiz:category-create', quiz_id=quiz.id)

        return HttpResponse('Creating Quiz Link!')




"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def QuizUpdate(request, quiz_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related('fourChoicesQuestions', 'trueOrFalseQuestions').get(id=quiz_id)
    if user != quiz.user:
        return HttpResponseForbidden()
    
    form = NewQuizForm(instance=quiz)
    if request.method == 'POST':
        form = NewQuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            # quiz.description = mark_safe(quiz.description)
            # quiz.save()s
            for q in quiz.fourChoicesQuestions.all():
                q.age_from = quiz.age_from
                q.age_to = quiz.age_to
                q.save()
            for q in quiz.trueOrFalseQuestions.all():
                q.age_from = quiz.age_from
                q.age_to = quiz.age_to
                q.save()
            profile = user.profile
            """
            Add this part to the question create and category create
            """
            # for category in quiz.categories.all():
            #     for question in quiz.fourChoicesQuestions.all():
            #         if category not in question.categories.all():
            #             question.categories.add(category)
            #     for category in question.categories.all():
            #         if category not in quiz.categories.all():
            #             question.categories.remove(category)
            #     for question in quiz.trueOrFalseQuestions.all():
            #         if category not in question.categories.all():
            #             question.categories.add(category)
            #     for category in question.categories.all():
            #         if category not in quiz.categories.all():
            #             question.categories.remove(category)


            #     question.categories.add(category)

            return redirect('quiz:quiz-detail', quiz_id=quiz.id, quiz_slug=quiz.slug, ref_code=profile.code)
            return redirect('quiz:create-quiz-link', quiz_id=quiz.id)
    
    context= {
        'form': form,
        'quiz': quiz,
    }

    return render(request, 'quiz/quizCreate.html', context)






# create the quiz delete view
@login_required(redirect_field_name='next', login_url='account_login')
def DeleteQuiz(request, quiz_id):
    try:
        user = request.user
        quiz = Quiz.objects.get(id=quiz_id)
        # quiz = get_object_or_404(Quiz, id=quiz_id)
        if not quiz.user == user:
            return HttpResponseForbidden()
        # profile = Profile.objects.get(user=user)
        if request.method == 'POST':
            # profile.quizzes -= 1
            # profile.likes -= 1
            # profile.save()
            quiz.is_active = False
            quiz.save()
            # quiz.delete()
            

            return HttpResponse('deleted!')
    except:
        return redirect('quiz:my-quizzes')
    


 


"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def QuestionCreate(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    profile = Profile.objects.get(user=user)

    context={
        'quiz': quiz,
        'profile': profile,
    }
    
    return render(request, 'quiz/newquestion.html', context)





@login_required(redirect_field_name='next', login_url='account_login')
def FourChoicesQuestionCreate(request, quiz_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related('categories', 'fourChoicesQuestions').get(id=quiz_id)
    form = NewFourChoicesQuestionForm()
    if request.method == 'POST':
        form = NewFourChoicesQuestionForm(request.POST)
        if form.is_valid():
            question= form.cleaned_data.get('question')
            answer1= form.cleaned_data.get('answer1')
            answer2= form.cleaned_data.get('answer2')
            answer3= form.cleaned_data.get('answer3')
            answer4= form.cleaned_data.get('answer4')
            correct=form.cleaned_data.get('correct')
            points=form.cleaned_data.get('points')
            duration_in_seconds=form.cleaned_data.get('duration_in_seconds')
            solution= form.cleaned_data.get('solution')
            shuffleAnswers = form.cleaned_data.get('shuffleAnswers')

            question = FourChoicesQuestion.objects.create(user=user, question=question,
            answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
            correct=correct, points=points, duration_in_seconds=duration_in_seconds, solution=solution, shuffleAnswers=shuffleAnswers)

            quiz.fourChoicesQuestions.add(question)
            quiz.lastQuestionIndex += 1
            quiz.questionLength += 1
            quiz.totalScore += question.points
            quiz.duration += question.duration_in_seconds
            quiz.save()
            question.index = quiz.lastQuestionIndex
            question.age_from = quiz.age_from
            question.age_to = quiz.age_to
            for category in quiz.categories.all():
                question.categories.add(category)
            question.save()

            return redirect('quiz:new-question', quiz_id=quiz.id)
    
    context= {
        'fourChoicesForm': form,
    }

    return render(request, 'question/fourChoicesQuestionCreate.html', context)






"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def TrueOrFalseQuestionCreate(request, quiz_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related('categories', 'trueOrFalseQuestions').get(id=quiz_id)
    form = NewTrueOrFalseQuestionForm()
    if request.method == 'POST':
        form = NewTrueOrFalseQuestionForm(request.POST)
        if form.is_valid():
            question= form.cleaned_data.get('question')
            correct=form.cleaned_data.get('correct')
            points=form.cleaned_data.get('points')
            duration_in_seconds=form.cleaned_data.get('duration_in_seconds')
            solution= form.cleaned_data.get('solution')


            question = TrueOrFalseQuestion.objects.create(user=user, question=question,correct=correct, points=points, solution=solution,
            duration_in_seconds=duration_in_seconds)

            quiz.trueOrFalseQuestions.add(question)
            quiz.lastQuestionIndex += 1
            quiz.questionLength += 1
            quiz.totalScore += question.points
            quiz.duration += question.duration_in_seconds
            quiz.save()
            question.index = quiz.lastQuestionIndex
            question.age_from = quiz.age_from
            question.age_to = quiz.age_to
            for category in quiz.categories.all():
               question.categories.add(category)
            question.save()
            return redirect('quiz:new-question', quiz_id=quiz.id)
    
    context= {
        'trueOrFalseForm': form,
    }
 
    return render(request, 'question/trueOrFalseQuestionCreate.html', context)





"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def FourChoicesQuestionUpdate(request, quiz_id, question_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related("categories").get(id=quiz_id)
    question = FourChoicesQuestion.objects.prefetch_related("categories").get(id=question_id)
    fourChoicesForm = NewFourChoicesQuestionForm(instance=question)
    if request.method == 'POST':

        form = NewFourChoicesQuestionForm(request.POST, instance=question)
        if form.is_valid():
            quiz.totalScore -= question.points
            quiz.duration -= question.duration_in_seconds
            instance = form.save()
            quiz.totalScore += instance.points
            quiz.duration += instance.duration_in_seconds
            quiz.save()
            for category in question.categories.all():
                question.categories.remove(category)

            for category in quiz.categories.all():
                question.categories.add(category)

            question.save()
            return redirect('quiz:quiz-detail', quiz_id=quiz.id, quiz_slug=quiz.slug, ref_code=user.profile.code)
    
    context= {
        'fourChoicesForm': fourChoicesForm,
    }

    return render(request, 'question/fourChoicesQuestionCreate.html', context)


@login_required(redirect_field_name='next', login_url='account_login')
def TrueOrFalseQuestionUpdate(request, quiz_id, question_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related('categories').get(id=quiz_id)
    question = TrueOrFalseQuestion.objects.prefetch_related('categories').get(id=question_id)
    trueOrFalseForm = NewTrueOrFalseQuestionForm(instance=question)
    if request.method == 'POST':
        form = NewTrueOrFalseQuestionForm(request.POST, instance=question)
        if form.is_valid():
            quiz.totalScore -= question.points
            quiz.duration -= question.duration_in_seconds
            instance = form.save()
            quiz.totalScore += instance.points
            quiz.duration += instance.duration_in_seconds
            quiz.save()

            for category in question.categories.all():
                question.categories.remove(category)

            for category in quiz.categories.all():
                question.categories.add(category)

            question.save()


            return redirect('quiz:quiz-detail', quiz_id=quiz.id, quiz_slug=quiz.slug, ref_code=user.profile.code)
    
    context= {
        'trueOrFalseForm': trueOrFalseForm,
    }

    return render(request, 'question/trueOrFalseQuestionCreate.html', context)




"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def CategoryCreate(request, quiz_id):
    user = request.user
    profile = Profile.objects.prefetch_related("categories").get(user=user)
    quiz = Quiz.objects.prefetch_related("categories").get(id=quiz_id)
    #make this part more efficient
    title = request.GET.get('newCategory') or ''
    title = slugify(title)
    if title:

        if quiz.categories.all().count() < 3:
            category = None
            try:
                category = Category.objects.get(title__iexact=title)
                if not category in quiz.categories.all():

                    quiz.categories.add(category)
                else:
                    messages.warning(request, _(f"{category.title} has already been added to the quiz!"))
            except:
                pass

            if not category:
                newCategory = Category.objects.create(registered_by=user, title=title, number_of_quizzes=1)
                quiz.categories.add(newCategory)
                if profile.categories.all().count() > 9:
                    removed = profile.categories.first()
                    profile.categories.remove(removed)
                profile.categories.add(newCategory)

                messages.success(request, _(f"{newCategory} has been added!"))



    addedCategory = request.GET.get("addedCategory") or ''
    if addedCategory:
        try:
            category = Category.objects.get(title__iexact=addedCategory) or None
            if category:

                while quiz.categories.count() > 2:
                    removed = quiz.categories.first()
                    quiz.categories.remove(removed)
                quiz.categories.add(category)

                if profile.categories.all().count() > 9:
                    removed = profile.categories.first()
                    profile.categories.remove(removed)
                profile.categories.add(category)
        except:
            pass



    # # create pagination
    # quizCategories = quiz.categories.all()
    # addedCategories = request.GET.getlist('addedCategories') or ''
    # if addedCategories:
        
    #     for category in quizCategories:
    #         # this is possible because __str__ returns the title of the category
    #         if category not in addedCategories:
    #             quiz.categories.remove(category)

    #     for cart in addedCategories:
    #         if quiz.categories.all().count() < 3:
    #             try:
    #                 category = Category.objects.get(title__iexact=cart) or None
    #                 if category:
    #                     if category not in quiz.categories.all():
    #                         quiz.categories.add(category)
    #                         if profile.categories.all().count() > 9:
    #                             removed = profile.categories.first()
    #                             profile.categories.remove(removed)
    #                         profile.categories.add(category)

    #             except:
    #                 pass
        
    quizCategories = quiz.categories.all()
    if request.GET.get('request_type') == 'ajax':
        # just use this place to return the json response
        print("Python just comes at you like motherfucker!")
        return JsonResponse({"categories":[x.title for x in quizCategories],
                            "category_count": quiz.categories.count(),})

    # categories = Category.objects.all().order_by('quiz_number_of_times_taken')[:20]
    # p = Paginator(categories, 20)
    # page = request.GET.get('page')
    # categories = p.get_page(page)

    context= {
        'page_obj': profile.categories.all(),# use profile categories here
        'objCategories' : quizCategories,
        'quiz': quiz,
        'obj_type': 'quiz',
    }

    return render(request, 'quiz/categoryCreate.html', context)



@login_required(redirect_field_name='next' ,login_url='account_login')
def CategoryRemove(request, quiz_id):
    quiz = Quiz.objects.prefetch_related('categories').get(id=quiz_id)
    category = request.GET.get('removedCategory')
    category = Category.objects.get(title=category)
    quiz.categories.remove(category)
    print('category removed')
    return JsonResponse({"categories":[x.title for x in quiz.categories.all()],
                        "category_count": quiz.categories.count(),})


@login_required(redirect_field_name='next' ,login_url='account_login')
def DeleteQuestion(request,quiz_id, question_form, question_id):
    user =request.user
    quiz = Quiz.objects.get(id=quiz_id)
    if question_form == 'fourChoices':
        question = FourChoicesQuestion.objects.get(id=question_id)
    elif question_form == 'trueOrFalse':
        question = TrueOrFalseQuestion.objects.get(id=question_id)
    if request.method == 'GET':

        quiz.questionLength -= 1
        quiz.totalScore -= question.points
        quiz.duration -= question.duration_in_seconds
        quiz.save()
        question.is_active = False
        question.save()
        # question.delete()

        return HttpResponse('You have deleted a question.')

    context={
        'obj': question,
    }

    return render(request, 'question/delete.html', context)




# the real test view
"""
Add all the documentation here

"""
def TakeQuiz(request, quiz_id):

    user = request.user
    quiz = Quiz.objects.prefetch_related('fourChoicesQuestions', 'trueOrFalseQuestions').get(id=quiz_id)
    profile = None
    if user.is_authenticated:
        # check if the coins is less than 3 to redirect to quiz generator
        profile = Profile.objects.get(user=user)
        messages.info(request,_("3 coins will be removed after submitting this quiz!"))
        
    preQuestions = []
    preQuestions += quiz.fourChoicesQuestions.all()
    preQuestions += quiz.trueOrFalseQuestions.all()
    questionsList = []
    for question in preQuestions:
        questionsList.append(tuple((question.index, question)))


    questionsList.sort(key=sortKey)
    questions = []
    for question in questionsList:
        questions.append(question[1])
    
    if quiz.shuffleQuestions:
        shuffle(questions)
    quiz.views += 1
    quiz.save()
    questions = enumerate(questions)
    context = {
        'user': user,
        'quiz': quiz,
        'questions': questions,
        'profile': profile,
    }
    return render(request, 'quiz/takequiz.html', context)







"""
create a lot of utilities for employees, like the one that will resolve the response of takenquiz
Give the full report of the quiz to the taker
all questions, questions taken, questions skipped, questions correct, questions wrong will be stored in your attempt model
handle all the questions that are not taken
all the report will be submitted to the creator of the questions too.
The total score should be adjusted whenever the creator the quiz updates the points of a question
"""
#totalScore, questionLength

def SubmitQuiz(request, quiz_id, *args, **kwargs):
    if request.method == 'GET':
        return redirect('quiz:take-quiz', quiz_id=quiz_id)
    
    user = request.user
    quiz = Quiz.objects.select_related('user').prefetch_related("categories", "likes").get(id=quiz_id)
    if not user.is_authenticated:
        code = str(kwargs.get('ref_code'))
        ReferralService(request, code)

    
        
    if user.is_authenticated:
        profile = Profile.objects.select_related('user').prefetch_related("categories", "quizTaken", "fourChoicesQuestionsTaken","fourChoicesQuestionsMissed", "trueOrFalseQuestionsTaken", "trueOrFalseQuestionsMissed", "trueOrFalseQuestionsWareHouse", "fourChoicesQuestionsWareHouse").get(user=user)
    
    
    if request.method == 'POST':
        score = 0
        # if user.is_authenticated:
        #     streak = Streak.objects.get(profile=profile)

        points = request.POST.get('points')
        answers = request.POST.getlist('answer')
        TimeTaken = request.POST.get('timeTaken')
        minutesTaken = int(TimeTaken) // 60
        secondsTaken = int(TimeTaken) % 60

        timeTaken = f"The quiz was finished in {minutesTaken} min, {secondsTaken} sec."
        questionsList = []
  
        for answer in answers:
            combination = tuple(answer.split('|'))
            
            if combination[0] == 'fourChoicesQuestion':
                question = FourChoicesQuestion.objects.get(id=combination[1])
                pos = combination[2]
                answer = question.getAnswer(pos)



                question.attempts += 1
                question.views += 1
                
                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1
                elif pos == 'answer3':
                    question.answer3NumberOfTimesTaken += 1
                elif pos == 'answer4':
                    question.answer4NumberOfTimesTaken += 1




                questionsList.append((question, answer))
                if question.correct == combination[2]:
                    score += question.points
                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)
                    if user.is_authenticated:
                        profile.fourChoicesQuestionsWareHouse.add(question)
                        if profile.fourChoicesQuestionsTaken.all().count() > 999:
                            removed = profile.fourChoicesQuestionsTaken.first()
                            profile.fourChoicesQuestionsTaken.remove(removed)
                        profile.fourChoicesQuestionsTaken.add(question)
                    
                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)
                    if user.is_authenticated:
                        profile.fourChoicesQuestionsWareHouse.add(question)
                        if profile.fourChoicesQuestionsMissed.all().count() > 999:
                            removed = profile.fourChoicesQuestionsMissed.first()
                            profile.fourChoicesQuestionsMissed.remove(removed)
                        profile.fourChoicesQuestionsMissed.add(question)
                    

                          

                question.save()

            elif combination[0] == 'trueOrFalseQuestion':
                question = TrueOrFalseQuestion.objects.get(id=combination[1])
                pos = combination[2]
                answer = question.getAnswer(pos)


                
                question.attempts += 1
                question.views += 1
                
                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1


                questionsList.append((question, answer))
                if question.correct == answer:
                    score += question.points
                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)
                    if user.is_authenticated:
                        profile.trueOrFalseQuestionsWareHouse.add(question)
                        if profile.trueOrFalseQuestionsTaken.all().count() > 999:
                            removed = profile.trueOrFalseQuestionsTaken.first()
                            profile.trueOrFalseQuestionsTaken.remove(removed)
                        profile.trueOrFalseQuestionsTaken.add(question)
                    
                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)


                    if user.is_authenticated:
                        profile.trueOrFalseQuestionsWareHouse.add(question)
                        if profile.trueOrFalseQuestionsMissed.all().count() > 999:
                            removed = profile.trueOrFalseQuestionsMissed.first()
                            profile.trueOrFalseQuestionsMissed.remove(removed)
                        profile.trueOrFalseQuestionsMissed.add(question)
                    




                question.save()
        try:
            total_score = quiz.totalScore
            user_score = score
            user_avg_score = (user_score/total_score) * 100

            if user.is_authenticated:
                
                    quiz.attempts += 1 # add this back below user_avg_score when attempters are fully in use

                    if quiz.user != profile.user:
                        # StreakValidator.delay(profile, user_score)
                        if user_avg_score >= 50:
                            creator = Profile.objects.get(user=quiz.user)
                            for category in quiz.categories.all():
                                if category not in profile.categories.all():
                                    if profile.categories.all().count() > 9:
                                        removed = profile.categories.first()
                                        profile.categories.remove(removed)
                                    profile.categories.add(category)

                        if quiz not in profile.quizTaken.all():
                            value = generateCoins(decimal.Decimal(user_avg_score), quiz.average_score, quiz.questionLength  )
                            
                            # value = round(((decimal.Decimal(user_avg_score)/100 + 1)**3) *(1 - (quiz.average_score/100)) * decimal.Decimal(user_score),0) + 5
                            profile.coins += value - 3
                            profile.save()

                            """
                            This is a celery tasks
                            don't remove the previous task ooo because it is different from this celery task
                            """
                            # CoinsTransaction.delay(user, value)

                            creator.coins += 1
                            creator.save()
                            # CreatorCoins.delay(creator.user, 1)

                            messages.success(request, f"You've won {value} coins!")
                            messages.info(request, f"3 coins have been deducted from your bonus!")
                        # else:
                        #     value = 5
                        #     profile.coins += value 
                        #     profile.save()
                        #     messages.success(request, f"You've won {value} coins!")

                            """
                            This is a celery tasks
                            don't remove the previous task ooo because it is different from this celery task
                            """
                            # CoinsTransaction.delay(user, value -5)



                    quiz.average_score = round(((quiz.average_score *(quiz.attempts - 1) + decimal.Decimal(user_avg_score)) / quiz.attempts), 1)
                    quiz.save()
                    if quiz not in profile.quizTaken.all():
                        if profile.quizTaken.all().count() > 999:
                            removed = profile.quizTaken.first()
                            profile.quizTaken.remove(removed)
                        profile.quizTaken.add(quiz)
                        if quiz.user != profile.user:
                            Attempter.objects.create(user=user, quiz=quiz, score=user_score, percentage=user_avg_score, timeTaken=TimeTaken)

                    profile.quizAttempts += 1
                    profile.quizAvgScore = decimal.Decimal(round(((profile.quizAvgScore * (profile.quizAttempts - 1) + decimal.Decimal(user_avg_score)) / profile.quizAttempts), 1))

                    profile.save()
            else:
                if score > 0:
                    user_score = score
                else:
                    messages.error(request, _("You didn't answer any question."))
                    return redirect('question:answer-question')
        except ZeroDivisionError:
            messages.error(request, _("You didn't answer any question."))
            return redirect('quiz:take-quiz', quiz_id = quiz.id)
                

        for category in quiz.categories.all():
            category.quiz_number_of_times_taken += 1
            category.save()

        avgScore = round(quiz.average_score, 2)
        
        attempt_report = _(f"You answered {len(answers)} out of {quiz.questionLength} questions")

    
        context = {
            "user": user,
            'quiz': quiz,
            'user_score': user_score,
            'user_avg_score': user_avg_score,
            'total_score': total_score,
            'questionsList': questionsList,
            'postAd': getAd('submit'),
            'page': 'submit',
            'avgScore': avgScore,
            'attempt_report': attempt_report,
            'timeTaken' : timeTaken,
        }

        try:
            if quiz.quizlink.name and quiz.quizlink.link and quiz.quizlink.description and not quiz.quizlink.ban:

                context['quizLink'] = quiz.quizlink
        except:
            pass

        try:
            attempters = quiz.attempters.all()[:10]
            context['attempters'] = attempters
        except:
            pass

    return render(request, 'quiz/submitQuiz.html', context)








@login_required(redirect_field_name='next', login_url='account_login')
def SolutionQuality(request, quiz_id):
    user = request.user
    if user.is_authenticated:
        quiz = Quiz.objects.prefetch_related('solution_validators').get(id=quiz_id)

        quality = request.GET.get('quality')
        print(quality)

        if quality == 'Yes':
            quiz.solution_quality += 1
            quiz.solution_validators.add(user)

        elif quality == 'No':
            quiz.solution_quality -= 1
            quiz.solution_validators.add(user)
        
        quiz.save()

    return HttpResponse('Modified Solution Quality!')






class QuizLinkClickCounter(View):
    def get(self, request, quizlink_id):
        quizLink = QuizLink.objects.get(id=quizlink_id)

        quizLink.clicks += 1
        quizLink.save()
        return HttpResponse('Quiz Link Clicked!')



class ReportLink(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quizLink_id = self.request.POST.get('quizlink_id')
        user = self.request.POST.get('user')
        quizLink = QuizLink.objects.get(id=quizLink_id)
        quizLink.reportCount += 1
        quizLink.reporters.add(user)

        if not quizLink.ban:        
            if quizLink.reportCount >= 10:
                quizLink.ban = True

        quizLink.save()

        return HttpResponse('The link has been reported!')












