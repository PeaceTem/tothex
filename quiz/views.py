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

from core.services import ReferralService
from .services import reverseStringCleaningService, ScoreRange

# Utilities
import random
from random import shuffle
from .utils import render_to_pdf, sortKey, quizRandomCoin, randomChoice, sortQuiz

import decimal




def CustomCheckbox(request):
    return render(request, 'quiz/custom-checkbox.html')


"""
Create a page for only users that are not logged in to taste the fun of the app before signing up
"""

class GeneratePDF(LoginRequiredMixin, View):

    def get(self, request, quiz_id, **kwargs):
        user = self.request.user
        number_of_registered_users = Profile.objects.all().count()
        template = get_template('quiz/takequiz.html')
        quiz = get_object_or_404(Quiz, id=quiz_id)

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

        html = template.render(context)
        pdf = render_to_pdf('quiz/quizPdf.html', context)

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"ToTheX_quiz_{quiz.title}.pdf"
            # content = f"inline; filename={filename}"
            content = f"attachment; filename={filename}"
            response['Content-Disposition'] = content

            return response
        return HttpResponse("Not Found!")



# the details of a quiz

def QuizDetail(request, quiz_id, *args, **kwargs):
    try:
        user = request.user
        quiz = Quiz.objects.get(id=quiz_id)
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
            device = request.META["HTTP_USER_AGENT"]
            ReferralService(device, code)
        
        postAd = PostAd.objects.all()
        if postAd.count() > 0:
            postAd = randomChoice(postAd)
            postAd.views += 1
            postAd.detailpageviews += 1
            postAd.save()
    except:
        return redirect('quiz:my-quizzes')    
    context = {
        'quiz': quiz,
        'user': user,
        'postAd': postAd,
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
        attempters = quiz.attempter_set.select_related('user').all()[:10]
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
@login_required(redirect_field_name='next', login_url='account_login')
def QuizList(request):
    user = request.user
    profile = Profile.objects.prefetch_related('categories', 'quizTaken').get(user=user)
    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2

    search_input= request.GET.get('search-area') or ''
    if search_input:
        quizzes = Quiz.objects.none()
        search = search_input.strip()
        search = search.split()
        for search_word in search:
            lookup =  Q(title__icontains=search_word) | Q(description__icontains=search_word) | Q(categories__title__icontains=search_word) | Q(user__username__icontains=search_word)
            quizzes |= Quiz.objects.filter(lookup).order_by("-relevance")
        
        quizzes = quizzes.order_by('-relevance').distinct()[:100]
    else:
        recommendedQuizzes = request.session.get('recommendedQuizzes') or []

        if len(recommendedQuizzes) > 0:
            print(request.session.get("recommendedQuizzes"), "Gotten!!!!")
            quizzes = recommendedQuizzes[:2]
            request.session["recommendedQuizzes"] = recommendedQuizzes[1:]
        else:


            age = profile.get_user_age
            # quizzes = Quiz.objects.none()
            categories = profile.categories.all()
            # for category in profile.categories.all():
            lookup = Q(categories__in=categories) & Q(age_from__lte=age) & Q(age_to__gte=age) #& Q(questionLength__gte=3)
            quizzes = Quiz.objects.filter(lookup).distinct()
            print(quizzes)
            takenQuiz = profile.quizTaken.all()
            randomQuizzes = []
            level1 = 0
            level2 = 0
            level3 = 0
            level4 = 0
            while quizzes.count() > 0:
                quiz =  randomChoice(quizzes)
                quizzes = quizzes.exclude(id=quiz.id)
                if quiz not in takenQuiz:
                    if quiz.relevance >= 0 and quiz.relevance <= 50 and level1 < 10:
                        randomQuizzes.append(quiz)
                        level1 += 1
                    elif quiz.relevance > 50 and quiz.relevance <= 150 and level2 < 20:
                        randomQuizzes.append(quiz)
                        level2 += 1
                    elif quiz.relevance > 150 and quiz.relevance <= 300 and level3 < 30:
                        randomQuizzes.append(quiz)
                        level3 += 1
                    elif quiz.relevance > 300 and level4 < 40:
                        randomQuizzes.append(quiz)
                        level4 += 1
            recommendedQuizzes = []
            for q in randomQuizzes:
                average_score = round(q.average_score)
                categories = []
                container = {
                    "id":q.id,
                    "user": q.user.username,
                    "title": q.title,
                    "description":q.description,
                    "when": q.when,
                    "questionLength": q.questionLength,
                    "attempts": q.attempts,
                    "average_score": average_score,
                    "get_duration": q.get_duration,
                    "likeCount": q.likeCount,
                    "age_from": q.age_from,
                    "age_to": q.age_to,
                }

                recommendedQuizzes.append(container)

            print("randomQuizzes Quizzes", randomQuizzes)

            quizzes = recommendedQuizzes[:2]
            request.session["recommendedQuizzes"] = recommendedQuizzes[1:]
    p = Paginator(quizzes, 1)
    page = request.GET.get('page')
    page = 1
    quizzes = p.get_page(page)
    context={

        'search_input': search_input,
        'page_obj': quizzes,
        'profile': profile,
        'nav': 'quizzes',
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
    }


    return render(request, 'quiz/quizzes_list.html', context)




@login_required(redirect_field_name='next', login_url='account_login')
def FollowerQuizList(request):
    user = request.user
    follow = Follower.objects.get(user=user)
    profile = Profile.objects.prefetch_related('quizTaken').get(user=user)
    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2
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
        print('The fetch has started!')
        while len(randomQuizzes) < 100 and quizzes.count() > 0:
            quiz = randomChoice(quizzes)
            print(quiz)
            quizzes = quizzes.exclude(id=quiz.id)
            if quiz not in takenQuiz:
                print('The quiz is not in quizTaken!')
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
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
    }


    return render(request, 'quiz/quizzes_list.html', context)





@login_required(redirect_field_name='next', login_url='account_login')
def MyQuizList(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    quizzes = User.quiz_set.all()
    # quizzes = Quiz.objects.get_user_quizzes(user)

    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2

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
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
    }


    return render(request, 'quiz/quizzes_list.html', context)



def VisitorView(request, owner_id):
    user = User.objects.get(id=owner_id)
    profile = Profile.objects.get(user=user)
    quizzes = Quiz.objects.get_user_quizzes(user)

    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2

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
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
    }


    return render(request, 'quiz/quizzes_list.html', context)








@login_required(redirect_field_name='next', login_url='account_login')
def QuizTakenList(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    number_of_registered_users = Profile.objects.prefetch_related('quizTaken').all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2

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
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
    }


    return render(request, 'quiz/quizzes_list.html', context)





@login_required(redirect_field_name='next', login_url='account_login')
def FavoriteQuizList(request):
    user = request.user
    profile = Profile.objects.prefetch_related('favoriteQuizzes').get(user=user)
    quizzes = profile.favoriteQuizzes.all()
    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2

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
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
    }
    return render(request, 'quiz/quizzes_list.html', context)








@login_required(redirect_field_name='next', login_url='account_login')
def CategoryQuizList(request, category):
    quizzes = Quiz.objects.filter(categories__title=category, relevance__gte=51).order_by("solution_quality")[:100]
    user = request.user
    profile = Profile.objects.get(user=user)
    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()

    number_of_questions_created = q1 + q2


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
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
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
        quiz = Quiz.objects.select_related('user').get(id=quiz_id)
        profile = Profile.objects.get(user=quiz.user)
        likeProfile = Profile.objects.prefetch_related('favoriteQuizzes').get(user=user)


        if user in quiz.likes.all():
            quiz.likes.remove(user)
            quiz.likeCount -= 1
            profile.likes -= 1
            likeProfile.favoriteQuizzes.remove(quiz)
            likeProfile.save()
            quiz.save()
            profile.save()
            return HttpResponse('unliked')

        else:
            quiz.likes.add(user)
            profile.likes += 1
            quiz.likeCount += 1
            likeProfile.favoriteQuizzes.add(quiz)
            quiz.save()
            profile.save()

            return HttpResponse('liked')


        """
        This is a celery command
        Remove this from the celery tasks
        """

        LikeQuiz.delay(quiz_id, user)





class RandomQuizPicker(LoginRequiredMixin, View):
    def get(self, request):
        print(self.request.META["HTTP_USER_AGENT"])
        user = self.request.user
        profile = Profile.objects.prefetch_related("categories").get(user=user)
        categories = profile.categories.all()
        quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=10, solution_quality__gt=3, average_score__gte=50).distinct()[:100]
        quiz = None
        if not quizzes.count() > 0:
            quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=10, solution_quality__gt=0).distinct()[:100]

        
        if not quizzes.count() > 0:
            quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=10)[:100]

        if quizzes.count() > 0:
            quiz = randomChoice(quizzes)

        if not quiz:
            messages.error(self.request, 'There is no quiz available')
            return redirect('quiz:quizzes')
        return redirect('quiz:take-quiz', quiz_id=quiz.id)







"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def QuizCreate(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = NewQuizForm()
    print(form)
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
            # return redirect('quiz:new-question', quiz_id=quiz.id)
            return redirect('quiz:create-quiz-link', quiz_id=quiz.id)
    
    context= {
        'form': form,
    }

    return render(request, 'quiz/quizCreate.html', context)



# use create view later
class QuizLinkCreate(LoginRequiredMixin, View):

    def get(self, request, quiz_id, *args, **kwargs):
        quiz = Quiz.objects.select_related('quizlink').get(id=quiz_id)
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
                    messages.error(self.request, 'You are not authorize to add a link')
                    return redirect('quiz:quizzes')
                try:
                    if quiz.quizlink:
                        messages.warning(self.request, 'You have already added a link to this quiz!')
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
            messages.error(self.request, 'An error occurred!')
            return redirect('quiz:category-create', quiz_id=quiz.id)

        return HttpResponse('Creating Quiz Link!')




"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def QuizUpdate(request, quiz_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related('fourChoicesQuestions', 'trueOrFalseQuestions').get(id=quiz_id)
    quiz.description = reverseStringCleaningService(quiz.description)
    if user != quiz.user:
        return HttpResponseForbidden()
    
    form = NewQuizForm(instance=quiz)
    if request.method == 'POST':
        form = NewQuizForm(request.POST, instance=quiz)
        if form.is_valid():
            quiz = form.save()
            quiz.description = mark_safe(quiz.description)
            quiz.save()
            for q in quiz.fourChoicesQuestions.all():
                q.age_from = quiz.age_from
                q.age_to = quiz.age_to
                q.save()
            for q in quiz.trueOrFalseQuestions.all():
                q.age_from = quiz.age_from
                q.age_to = quiz.age_to
                q.save()
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
        profile = Profile.objects.get(user=user)
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if request.method == 'POST':
            profile.quizzes -= 1
            profile.save()
            quiz.delete()

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
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = NewFourChoicesQuestionForm()
    if request.method == 'POST':
        form = NewFourChoicesQuestionForm(request.POST)
        if form.is_valid():
            question= form.cleaned_data.get('question')
            answer1=form.cleaned_data.get('answer1')
            answer2=form.cleaned_data.get('answer2')
            answer3=form.cleaned_data.get('answer3')
            answer4=form.cleaned_data.get('answer4')
            correct=form.cleaned_data.get('correct')
            points=form.cleaned_data.get('points')
            duration_in_seconds=form.cleaned_data.get('duration_in_seconds')
            solution=form.cleaned_data.get('solution')
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

    return render(request, 'quiz/fourChoicesQuestionCreate.html', context)






"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def TrueOrFalseQuestionCreate(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = NewTrueOrFalseQuestionForm()
    if request.method == 'POST':
        form = NewTrueOrFalseQuestionForm(request.POST)
        if form.is_valid():
            question= form.cleaned_data.get('question')
            answer1=form.cleaned_data.get('answer1')
            answer2=form.cleaned_data.get('answer2')
            correct=form.cleaned_data.get('correct')
            points=form.cleaned_data.get('points')
            duration_in_seconds=form.cleaned_data.get('duration_in_seconds')
            solution=form.cleaned_data.get('solution')


            question = TrueOrFalseQuestion.objects.create(user=user, question=question,
            correct=correct, points=points, solution=solution, duration_in_seconds=duration_in_seconds)

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

    return render(request, 'quiz/trueOrFalseQuestionCreate.html', context)





"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def FourChoicesQuestionUpdate(request, quiz_id, question_id):
    user = request.user
    quiz = Quiz.objects.prefetch_related("categories").get(id=quiz_id)
    question = FourChoicesQuestion.objects.prefetch_related("categories").get(id=question_id)
    question.question = reverseStringCleaningService(question.question)
    question.answer1 = reverseStringCleaningService(question.answer1)
    question.answer2 = reverseStringCleaningService(question.answer2)
    question.answer3 = reverseStringCleaningService(question.answer3)
    question.answer4 = reverseStringCleaningService(question.answer4)
    question.solution = reverseStringCleaningService(question.solution)
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
            return redirect('quiz:quiz-detail', quiz_id=quiz.id, ref_code=user.profile.code)
    
    context= {
        'fourChoicesForm': fourChoicesForm,
    }

    return render(request, 'quiz/fourChoicesQuestionCreate.html', context)


@login_required(redirect_field_name='next', login_url='account_login')
def TrueOrFalseQuestionUpdate(request, quiz_id, question_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(TrueOrFalseQuestion, id=question_id)
    question.question = reverseStringCleaningService(question.question)
    question.solution = reverseStringCleaningService(question.solution)
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


            return redirect('quiz:quiz-detail', quiz_id=quiz.id, ref_code=user.profile.code)
    
    context= {
        'trueOrFalseForm': trueOrFalseForm,
    }

    return render(request, 'quiz/trueOrFalseQuestionCreate.html', context)




"""
Add all the documentation here
"""
@login_required(redirect_field_name='next', login_url='account_login')
def CategoryCreate(request, quiz_id):
    user = request.user
    profile = Profile.objects.prefetch_related("categories").get(user=user)
    quiz = Quiz.objects.prefetch_related("categories").get(id=quiz_id)
    form = NewCategoryForm()
    categories = Category.objects.all()

    title = request.GET.get('newCategory') or ''
    title = title.strip()
    title = title.split(' ')
    title = '-'.join(title)
    if title:

        if quiz.categories.all().count() < 5:
            category = None
            try:
                category = Category.objects.get(title__iexact=title)
                if not category in quiz.categories.all():

                    quiz.categories.add(category)
                    quiz.save()
                    category.number_of_quizzes += 1
                    category.save()
                else:
                    messages.warning(request, f"{category.title} has already been added to the quiz!")
            except:
                pass

            if not category:
                newCategory = Category.objects.create(registered_by=user, title=title)
                quiz.categories.add(newCategory)
                quiz.save()
                newCategory.number_of_quizzes += 1
                newCategory.save()
                if profile.categories.all().count() > 99:
                    removed = profile.categories.first()
                    profile.categories.remove(removed)
                profile.categories.add(newCategory)
                profile.save()

                messages.success(request, f"{newCategory} has been added!")      



    # create pagination
    quizCategories = quiz.categories.all()
    addedCategories = request.GET.getlist('addedCategories') or ''
    if addedCategories:
        
        for category in quizCategories:
            if category not in addedCategories:
                quiz.categories.remove(category)
                category.number_of_quizzes -= 1
                category.save()

        for cart in addedCategories:
            if quiz.categories.all().count() < 5:
                category = Category.objects.get(title__iexact=cart) or None
                if category:
                    if category not in quiz.categories.all():
                        quiz.categories.add(category)
                        quiz.save()
                        category.number_of_quizzes += 1
                        category.save()
                        if profile.categories.all().count() > 99:
                            removed = profile.categories.first()
                            profile.categories.remove(removed)
                        profile.categories.add(category)
                        profile.save()


        
    quizCategories = quiz.categories.all()

    p = Paginator(categories, 100)
    page = request.GET.get('page')
    quizzes = p.get_page(page)

    context= {
        'page_obj': categories,
        'quizCategories' : quizCategories,
        'quiz': quiz,

    }

    return render(request, 'quiz/categoryCreate.html', context)




@login_required(redirect_field_name='next' ,login_url='account_login')
def DeleteQuestion(request,quiz_id, question_form, question_id):
    user =request.user
    quiz = Quiz.objects.get(id=qui_id)
    if question_form == 'fourChoices':
        question = FourChoicesQuestion.objects.get(id=question_id)
    elif question_form == 'trueOrFalse':
        question = TrueOrFalseQuestion.objects.get(id=question_id)
    if request.method == 'GET':

        quiz.questionLength -= 1
        quiz.totalScore -= question.points
        quiz.duration -= question.duration_in_seconds
        quiz.save()
        question.delete()
        messages.success(request, "You've successfully delete a question!")

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
    number_of_registered_users = Profile.objects.all().count()
    if user.is_authenticated:
        profile = Profile.objects.prefetch_related('quizTaken').get(user=user)
        
        if quiz not in profile.quizTaken.all():
            if profile.coins < 5:
                messages.error(request, "You don't have enough coins to take a quiz")
                messages.info(request, "Earn more coins by taking your quiz here!")
                return redirect('question:quiz-generator')
            profile.coins -= 5
            messages.info(request, '5 coins have been removed!')
            profile.save()






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
    context = {
        'user': user,
        'quiz': quiz,
        'questions': questions,
        'profile': profile,
        'number_of_registered_users' : number_of_registered_users,
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
        return redirect('quiz:take-quiz', quiz_id=quiz.id)
    
    user = request.user
    quiz = Quiz.objects.select_related('user').prefetch_related("categories").get(id=quiz_id)
    if not user.is_authenticated:
        code = str(kwargs.get('ref_code'))
        device = request.META["HTTP_USER_AGENT"]
        ReferralService(device, code)

    
        
    if user.is_authenticated:
        profile = Profile.objects.select_related('user').prefetch_related("categories", "quizTaken", "fourChoicesQuestionsTaken","fourChoicesQuestionsMissed", "TrueOrFalseQuestionsTaken", "TrueOrFalseQuestionsMissed" ).get(user=user)
    
    
    if request.method == 'POST':
        score = 0
        postAd = PostAd.objects.all()
        postAd = randomChoice(postAd)
        postAd.views += 1
        postAd.submitpageviews += 1
        postAd.save()
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
                        if profile.fourChoicesQuestionsTaken.all().count() > 999:
                            removed = profile.fourChoicesQuestionsTaken.first()
                            profile.fourChoicesQuestionsTaken.remove(removed)
                        profile.fourChoicesQuestionsTaken.add(question)
                    
                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)
                    if user.is_authenticated:
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
                
                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1


                questionsList.append((question, answer))
                if question.correct == answer:
                    score += question.points
                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)
                    if user.is_authenticated:
                        if profile.trueOrFalseQuestionsTaken.all().count() > 999:
                            removed = profile.trueOrFalseQuestionsTaken.first()
                            profile.trueOrFalseQuestionsTaken.remove(removed)
                        profile.trueOrFalseQuestionsTaken.add(question)
                    
                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)


                    if user.is_authenticated:
                        if profile.trueOrFalseQuestionsMissed.all().count() > 999:
                            removed = profile.trueOrFalseQuestionsMissed.first()
                            profile.trueOrFalseQuestionsMissed.remove(removed)
                        profile.trueOrFalseQuestionsMissed.add(question)
                    




                question.save()

        total_score = quiz.totalScore
        user_score = score
        if user.is_authenticated:
            try:

                quiz.attempts += 1
                user_avg_score = (user_score/total_score) * 100


                if quiz.user != profile.user:
                    StreakValidator.delay(profile, user_score)
                    if user_avg_score >= 50:
                        creator = Profile.objects.get(user=quiz.user)
                        for category in quiz.categories.all():
                            if category not in profile.categories.all():
                                if profile.categories.all().count() > 29:
                                    removed = profile.categories.first()
                                    profile.categories.remove(removed)
                                profile.categories.add(category)

                    if quiz not in profile.quizTaken.all():
                        value = generateCoins(decimal.Decimal(user_avg_score), quiz.average_score, quiz.questionLength)
                        # value = round(((decimal.Decimal(user_avg_score)/100 + 1)**3) *(1 - (quiz.average_score/100)) * decimal.Decimal(user_score),0) + 5
                        profile.coins += value
                        profile.save()

                        """
                        This is a celery tasks
                        don't remove the previous task ooo because it is different from this celery task
                        """
                        CoinsTransaction.delay(user, value)

                        creator.coins += 1
                        creator.save()
                        CreatorCoins.delay(creator.user, 1)
                        messages.success(request, f"You've won {value} coins!")
                    else:
                        value = 5
                        profile.coins += value 
                        profile.save()
                        messages.success(request, f"You've won {value} coins!")

                        """
                        This is a celery tasks
                        don't remove the previous task ooo because it is different from this celery task
                        """
                        CoinsTransaction.delay(user, value -5)



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
            except ZeroDivisionError:
                messages.error(request, "You didn't answer any question.")
                return redirect('quiz:take-quiz', quiz_id = quiz.id)
        else:
            if score > 0:
                user_score = score
            else:
                messages.error(request, "You didn't answer any question.")
                return redirect('question:answer-question')
        

        for category in quiz.categories.all():
            category.quiz_number_of_times_taken += 1
            category.save()

        avgScore = round(quiz.average_score, 2)
        
        attempt_report = f"You answered {len(answers)} out of {quiz.questionLength} questions"

    
        context = {
            "user": user,
            'quiz': quiz,
            'user_score': user_score,
            'user_avg_score': user_avg_score,
            'total_score': total_score,
            'questionsList': questionsList,
            'postAd': postAd,
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
            attempters = quiz.attempter_set.select_related('user').all()[:10]
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
        print(quizLink_id, user)
        quizLink = QuizLink.objects.get(id=quizLink_id)
        print(quizLink)
        quizLink.reportCount += 1
        quizLink.reporters.add(user)

        if not quizLink.ban:        
            print(quizLink.ban)
            if quizLink.reportCount >= 10:
                print(quizLink.reportCount)
                quizLink.ban = True

        quizLink.save()

        return HttpResponse('The link has been reported!')
