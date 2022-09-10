from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse

from .models import TrueOrFalseQuestion, FourChoicesQuestion

from django.contrib.auth.decorators import login_required

from django.db.models import Q, F, Count, Avg, Min, Max, Sum

# the forms for each model
from .forms import NewFourChoicesQuestionForm, NewTrueOrFalseQuestionForm, QuizGeneratorForm
from category.forms import NewCategoryForm
# the models to be used to create the quiz app
from django.contrib.auth.models import User
from core.models import Streak, Profile, Follower
from category.models import Category
from ads.models import PostAd
from quiz.models import Quiz
# celery tasks
from core.tasks import StreakValidator, CoinsTransaction, CreatorCoins

# Utilities
from random import shuffle
from quiz.utils import sortKey, randomCoin, adsRandom, randomChoice
from question.utils import randomQuestions
import decimal
import math
#Paginator

from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
# django messages
from django.contrib import messages



from django.core import serializers
from django.forms.models import model_to_dict

import json
from django.utils.text import slugify

from core.services import ReferralService, get_user_ip
from ads.services import getAd
# from quiz.services import reverseStringCleaningService, stringCleaningService

# Create your views here.
"""
Generate image from the questions here.

"""


# the real test view
"""
Add all the documentation here

Whenever a question is created, an option to go live or add to draft should be presented to the user.
"""

# @login_required(redirect_field_name='next' ,login_url='account_login')
def Question(request):
    user = request.user
    number_of_registered_users = Profile.objects.all().count()
    number_of_quizzes_created = Quiz.objects.all().count()
    q1 = TrueOrFalseQuestion.objects.all().count()
    q2 = FourChoicesQuestion.objects.all().count()
    tq = TrueOrFalseQuestion.objects.aggregate(Sum('attempts'))
    # print('This is the sum that you are looking for: ', question_attempts)
    # print(question_attempts['attempts__sum'])
    fq = FourChoicesQuestion.objects.aggregate(Sum('attempts'))
    total_number_of_attempts = fq['attempts__sum'] + tq['attempts__sum']
    number_of_questions_created = q1 + q2
    profile = None
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
    context={
        'nav': 'questions',
        'profile': profile,
        'number_of_registered_users' : number_of_registered_users,
        'number_of_quizzes_created' : number_of_quizzes_created,
        'number_of_questions_created' : number_of_questions_created,
        'total_number_of_attempts' : total_number_of_attempts,
    }

    return render(request, 'question/questions.html', context)




@login_required(redirect_field_name='next' ,login_url='account_login')
def MyQuestionList(request):
    user = request.user
    preQuestions = []
    preQuestions += FourChoicesQuestion.objects.select_related("user").filter(user=user, is_active=True, standalone=True)
    preQuestions += TrueOrFalseQuestion.objects.select_related("user").filter(user=user, is_active=True, standalone=True)
    questions = []
    # total_question_attempts = 0
    for question in preQuestions:
        questions.append(tuple((question.date_created, question)))
        # total_question_attempts += question.attempts

    questions.sort(key=sortKey, reverse=True)
    # add reverse later
    total_views = sum([x[1].views for x in questions])
    total_question_attempts = sum([x[1].attempts for x in questions])
    questions_length = len(questions)
    p = Paginator(questions, 10)
    page = request.GET.get('page')
    questions = p.get_page(page)


    context={
        'owner': user,
        'user': user,
        'nav': 'my-questions',
        'page_obj': questions,
        "viewer": "owner",
        "total_question_attempts": total_question_attempts,
        # 'average_attempts': average_attempts,
        # 'average_views': average_views,
        'total_questions_created':questions_length,
        'total_views': total_views,
    }
    try:
        average_attempts = round(total_question_attempts/questions_length, 2)
        average_views = round(total_views/questions_length, 2)
        context['average_attempts'] = average_attempts
        context['average_views'] = average_views
    except ZeroDivisionError:
        pass
    
    return render(request, 'question/myquestions.html', context)




def VisitorView(request, owner_id):
    owner = User.objects.get(id=owner_id)
    preQuestions = []
    preQuestions += FourChoicesQuestion.objects.select_related("user").filter(user=owner, is_active=True, standalone=True)
    preQuestions += TrueOrFalseQuestion.objects.select_related("user").filter(user=owner, is_active=True, standalone=True)
    questions = []
    for question in preQuestions:
        questions.append(tuple((question.date_created, question)))


    questions.sort(key=sortKey, reverse=True)
    questions_length = len(questions)
    total_question_attempts = sum([x[1].attempts for x in questions])
    total_views = sum([x[1].views for x in questions])

    p = Paginator(questions, 10)
    page = request.GET.get('page')
    questions = p.get_page(page)
    """
    
    Add the average attempts and average views to this one also
    """
    
    try:
        average_attempts = round(total_question_attempts/questions_length, 2)
        average_views = round(total_views/questions_length, 2)
    except ZeroDivisionError:
        pass

    context={
        'owner': owner,
        'user':request.user,
        'nav': 'my-questions',
        'page_obj': questions,
        "viewer": "visitor",
        "total_question_attempts": total_question_attempts,
        'average_attempts': average_attempts,
        'average_views': average_views,
        'total_questions_created':questions_length,
        'total_views': total_views,
    }

    return render(request, 'question/myquestions.html', context)





def AnswerQuestion(request):

    user = request.user
    question_type = randomChoice(['fourChoices', 'trueOrFalse'])
    creator = request.GET.get('creator')
    if creator:
        creator = User.objects.get(username=creator)
        question = None
        if question_type == 'fourChoices':
            fqs = creator.fourChoicesQuestions.filter(is_active=True)
            if fqs.count()>0:
                question = randomChoice(fqs)
        elif question_type == 'trueOrFalse':
            tfqs = creator.trueOrFalseQuestions.filter(is_active=True)
            if tfqs.count()>0:
                question = randomChoice(tfqs)
        
        if not question:

            return redirect('question:visitor', owner_id=creator.id)
        score = round((2 - question.avgScore/100) * 2, 2)
        question.views += 1  
        question.save() 
        context = {
        'question': question,
        'score'  : score,
        'questionType' : 'OldTownRoad',
        'creator' : creator,
        }
        
        if question.form == "fourChoicesQuestion":
            # check if you are to shuffle this question's answers
            ans = [1,2,3,4]
            shuffle(ans)
            context["ans"] = ans
        return render(request, 'question/takequestion.html', context)
    if user.is_authenticated:
        if question_type == 'fourChoices':
            # the profile should only prefetch recommended questions alone
            # print('Entering the first step')
            profile = Profile.objects.prefetch_related('recommended_four_choices_questions').get(user=user)
            if profile.coins < 1:
                messages.info(request, _("You'll get 1 coin here"))
                return redirect('ads:postAd', nextpage='oldtownroad')
            if profile.recommended_four_choices_questions.count() < 1:
                # print('Entering the funnel!')

                profile = Profile.objects.prefetch_related('categories', 'fourChoicesQuestionsMissed', 'fourChoicesQuestionsTaken', 'recommended_four_choices_questions').get(user=user)

                categories = profile.categories.all()
                age = profile.get_user_age
                lookup = Q(is_active=True) &  Q(relevance__gte=0) & Q(age_from__lte=age) & Q(age_to__gte=age) & Q(standalone=True)
                questionsList = (*profile.fourChoicesQuestionsMissed.all(), *profile.fourChoicesQuestionsTaken.all(),)
                while categories.count() >= 1 and profile.recommended_four_choices_questions.count() <= 150:
                    category = randomChoice(categories)
                    categories = categories.exclude(id=category.id)
                    questions = (*category.fourChoicesQuestions.filter(lookup)[:200],)
                    # print(category)
                
                    for q in questions:
                        # print(q)
                        if q not in questionsList:
                            profile.recommended_four_choices_questions.add(q)
                            if profile.recommended_four_choices_questions.count() >= 150:
                                break
                
            if profile.recommended_four_choices_questions.count() > 0:
                # print('Entering the easier steps!')

                question = randomChoice(profile.recommended_four_choices_questions.all())
                profile.recommended_four_choices_questions.remove(question)
                # print('From recommended')
            else:
                messages.info(request, _('The questions are insufficient!'))
                return redirect("question:questions")
            # change the recommendation algorithm to bucket based
            
        elif question_type == 'trueOrFalse':
            profile = Profile.objects.prefetch_related('recommended_true_or_false_questions').get(user=user)
            # print('First step')
            if profile.coins < 1:
                return redirect('ads:postAd', nextpage='oldtownroad')
            if profile.recommended_true_or_false_questions.count() < 1:
                # print('entering the funnel')
                profile = Profile.objects.prefetch_related("categories","trueOrFalseQuestionsMissed","trueOrFalseQuestionsTaken",'recommended_true_or_false_questions').get(user=user)

                categories = profile.categories.all()
                age = profile.get_user_age
                lookup = Q(is_active=True) & Q(relevance__gte=0) & Q(age_from__lte=age) & Q(age_to__gte=age) & Q(standalone=True)
                questionsList = (*profile.trueOrFalseQuestionsMissed.all(), *profile.trueOrFalseQuestionsTaken.all(),)
                while categories.count() > 1 and profile.recommended_true_or_false_questions.count() <= 150:
                    category = randomChoice(categories)
                    categories = categories.exclude(id=category.id)
                    questions = (*category.trueOrFalseQuestions.filter(lookup)[:200],)
                    # print(category)
                    # print('This is the questions', questions)
                    for q in questions:
                        # print(q)
                        if q not in questionsList:
                            profile.recommended_true_or_false_questions.add(q)
                            if profile.recommended_true_or_false_questions.count() >= 150:
                                break

            if profile.recommended_true_or_false_questions.count() > 0:
                # print('Entering the easier steps!')
                question = randomChoice(profile.recommended_true_or_false_questions.all())
                profile.recommended_true_or_false_questions.remove(question)
                # print('From recommended')
            else:
                messages.info(request, _('The questions are insufficient!'))
                return redirect("question:questions")
            # change the recommendation algorithm to bucket based
            


    else:
        if question_type == 'fourChoices':
            questions = FourChoicesQuestion.objects.filter(is_active=True, relevance__gte=0)[:100]
        elif question_type == 'trueOrFalse':
            questions = TrueOrFalseQuestion.objects.filter(is_active=True, relevance__gte=0)[:100]
        
        if questions.count() > 0:
            question = randomChoice(questions)
        else:
            messages.info(request, _('The questions are insufficient!'))
            return redirect("question:questions")
    score = round((2 - question.avgScore/100) * 2, 2)
    question.views += 1  
    question.save() 
    context = {
    'question': question,
    'score'  : score,
    'questionType' : 'OldTownRoad',
    }
    
    if question.form == "fourChoicesQuestion":
        # check if you are to shuffle this question's answers
        ans = [1,2,3,4]
        shuffle(ans)
        context["ans"] = ans
    return render(request, 'question/takequestion.html', context)




@login_required(redirect_field_name='next' ,login_url='account_login')
def FollowingQuestion(request):
    user = request.user
    question_type = randomChoice(['fourChoices', 'trueOrFalse'])

    if question_type == 'fourChoices':
        # print('Entering the first step')
        profile = Profile.objects.prefetch_related('following_four_choices_questions').get(user=user)
        if profile.coins < 1:
            messages.info(request, _("You'll get 1 coin here"))
            return redirect('ads:postAd', nextpage='following')
        if profile.following_four_choices_questions.count() < 1:
            # print('Entering the funnel!')

            profile = Profile.objects.prefetch_related('fourChoicesQuestionsMissed', 'fourChoicesQuestionsTaken', 'following_four_choices_questions').get(user=user)
            follower = Follower.objects.prefetch_related('following').get(user=user)
            following = follower.following.prefetch_related('fourChoicesQuestions').all()#  filter this part of the code

            questionsList = (*profile.trueOrFalseQuestionsMissed.all(), *profile.trueOrFalseQuestionsTaken.all(),)
            
            while following.count() > 0 and profile.following_four_choices_questions.count() <= 150:
                f = randomChoice(following)
                following = following.exclude(id=f.id)
                questions = f.fourChoicesQuestions.filter(is_active=True, standalone=True)
                for q in questions:
                    if q not in questionsList:
                        profile.following_four_choices_questions.add(q)
                        if profile.following_four_choices_questions.count() >= 150:
                            break

        if profile.following_four_choices_questions.count() > 0:
            # print('Entering the easier steps!')

            question = randomChoice(profile.following_four_choices_questions.all())
            profile.following_four_choices_questions.remove(question)
            # print('From recommended')
        else:
            messages.info(request, _('The questions are insufficient!'))
            return redirect("question:questions")
        # change the recommendation algorithm to bucket based
        
    elif question_type == 'trueOrFalse':
        profile = Profile.objects.prefetch_related('following_true_or_false_questions').get(user=user)
        # print('First step')
        if profile.coins < 1:
            return redirect('ads:postAd', nextpage='following')
        if profile.following_true_or_false_questions.count() < 1:
            # print('entering the funnel')
            profile = Profile.objects.prefetch_related("trueOrFalseQuestionsMissed","trueOrFalseQuestionsTaken",'following_true_or_false_questions').get(user=user)
            follower = Follower.objects.prefetch_related('following').get(user=user)
            following = follower.following.prefetch_related('trueOrFalseQuestions').all()
            questionsList = (*profile.trueOrFalseQuestionsMissed.all(), *profile.trueOrFalseQuestionsTaken.all(),)

            while following.count() > 0 and  profile.following_true_or_false_questions.count() <= 150:
                f = randomChoice(following)
                following = following.exclude(id=f.id)
                questions = f.trueOrFalseQuestions.filter(is_active=True, standalone=True)
                for q in questions:
                    if q not in questionsList:
                        profile.following_true_or_false_questions.add(q)
                        if profile.following_true_or_false_questions.count() >= 150:
                            break

        if profile.following_true_or_false_questions.count() > 0:
            # print('Entering the easier steps!')
            question = randomChoice(profile.following_true_or_false_questions.all())
            profile.following_true_or_false_questions.remove(question)
            # print('From recommended')
        else:
            messages.info(request, _('The questions are insufficient!'))
            return redirect("question:questions")
        # change the recommendation algorithm to bucket based
        
    question.views += 1  
    question.save()      
    score = round((2 - question.avgScore/100) * 2, 2)



    context = {
        'score': score,
        'question': question,
        'questionType' : 'Following',
    }
    if question.form == "fourChoicesQuestion":
        ans = [1,2,3,4]
        shuffle(ans)
        context["ans"] = ans
    return render(request, 'question/takequestion.html', context)



# def CovenQuestions():





def CorrectionView(request, question_form, question_id, qtype, answer):
    user = request.user
    creator = request.GET.get('creator')

    if question_form == 'fourChoicesQuestion':
        question = FourChoicesQuestion.objects.prefetch_related("solution_validators").select_related("user", "quiz").get(id=question_id)
    elif question_form == 'trueOrFalseQuestion':
        question = TrueOrFalseQuestion.objects.prefetch_related("solution_validators").select_related("user", "quiz").get(id=question_id)


    context={
        'user': user,
        'question': question,
        'questionType': qtype,
        'answer' : answer,
        'postAd': getAd('correction'),
        'page': 'correction',
        'creator': creator,
    }

    return render(request, 'question/correction.html', context)


"""
Add all the documentation here
"""
@login_required(redirect_field_name='next' ,login_url='account_login')
def QuestionCreate(request):
    return render(request, 'question/newquestion.html')





@login_required(redirect_field_name='next' ,login_url='account_login')
def FourChoicesQuestionCreate(request):
    user = request.user
    form = NewFourChoicesQuestionForm()
    if request.method == 'POST':
        form = NewFourChoicesQuestionForm(request.POST or None)
        if form.is_valid():
            question= form.cleaned_data.get('question')
            answer1= form.cleaned_data.get('answer1')
            answer2 = form.cleaned_data.get('answer2')
            answer3= form.cleaned_data.get('answer3')
            answer4= form.cleaned_data.get('answer4')
            correct=form.cleaned_data.get('correct')
            duration=form.cleaned_data.get('duration_in_seconds')
            solution= form.cleaned_data.get('solution')
            shuffleAnswers = form.cleaned_data.get('shuffleAnswers')
            age_from = form.cleaned_data.get('age_from')
            age_to = form.cleaned_data.get('age_to')
            question = FourChoicesQuestion.objects.create(user=user, question=question,
            answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
            correct=correct, duration_in_seconds=duration, solution=solution, shuffleAnswers=shuffleAnswers,
            age_from=age_from, age_to=age_to, standalone=True)


            return redirect('question:category-create', question_id=f'fourChoices-{question.id}')
    
    context= {
        'fourChoicesForm': form,
    }
    return render(request, 'question/fourChoicesQuestionCreate.html', context)






"""
Add all the documentation here
"""
@login_required(redirect_field_name='next' ,login_url='account_login')
def TrueOrFalseQuestionCreate(request):
    user = request.user
    form = NewTrueOrFalseQuestionForm()
    if request.method == 'POST':
        form = NewTrueOrFalseQuestionForm(request.POST or None)
        if form.is_valid(): 
            question= form.cleaned_data.get('question')
            correct=form.cleaned_data.get('correct')
            duration=form.cleaned_data.get('duration_in_seconds')
            solution= form.cleaned_data.get('solution')
            age_from = form.cleaned_data.get('age_from')
            age_to = form.cleaned_data.get('age_to')
            question = TrueOrFalseQuestion.objects.create(user=user, question=question,
            correct=correct, solution=solution, duration_in_seconds=duration, age_from=age_from, age_to=age_to, standalone=True)

            return redirect('question:category-create', question_id=f'trueOrFalse-{question.id}')

    
    context= {
        'trueOrFalseForm': form,
    }

    return render(request, 'question/trueOrFalseQuestionCreate.html', context)





"""
Add all the documentation here
"""
@login_required(redirect_field_name='next' ,login_url='account_login')
def CategoryCreate(request, question_id):
    q_id = question_id
    user = request.user
    profile = Profile.objects.prefetch_related("categories").get(user=user)
    question_id = question_id.split('-')
    if question_id[0] == 'trueOrFalse':
        question = TrueOrFalseQuestion.objects.prefetch_related("categories").get(id=question_id[1])
    elif question_id[0] == 'fourChoices':
        question = FourChoicesQuestion.objects.prefetch_related("categories").get(id=question_id[1])

    categories = Category.objects.all().order_by('question_number_of_times_taken')[:100]

    title = request.GET.get('newCategory') or ''
    title = slugify(title)
    if title:
        if question.categories.all().count() < 3:
            category = None

            try:
                newCategory = Category.objects.get(title__iexact=title)
                if not newCategory in question.categories.all():

                    question.categories.add(newCategory)
                    if profile.categories.all().count() > 9:
                        removed = profile.categories.first()
                        profile.categories.remove(removed)
                    profile.categories.add(newCategory)
                else:
                    messages.warning(request, _(f"{newCategory.title} has already been added to the question!"))
                # return a message that it is already created
            except:
                newCategory = Category.objects.create(registered_by=user, title=title)
                question.categories.add(newCategory)
                if profile.categories.all().count() > 9:
                    removed = profile.categories.first()
                    profile.categories.remove(removed)
                profile.categories.add(newCategory)


    # create pagination
    # addedCategories = request.GET.getlist('addedCategories') or ''
    # if addedCategories:
        
    #     for category in questionCategories:
    #         if category not in addedCategories:
    #             question.categories.remove(category)

    #     for cart in addedCategories:
    #         category = None
    #         if question.categories.all().count() < 3:
    #             try:
    #                 category = Category.objects.get(title__iexact=cart)
    #             except:
    #                 pass
    #             if category:
    #                 if category not in question.categories.all():
    #                     question.categories.add(category)
    #                     if profile.categories.all().count() > 9:
    #                         removed = profile.categories.first()
    #                         profile.categories.remove(removed)
    #                     profile.categories.add(category)

        
    questionCategories = question.categories.all()
    addedCategory = request.GET.get("addedCategory") or ''
    if addedCategory:
        try:
            category = Category.objects.get(title__iexact=addedCategory) or None
            if category:

                while question.categories.count() > 2:
                    removed = question.categories.first()
                    question.categories.remove(removed)
                question.categories.add(category)

                if profile.categories.all().count() > 9:
                    removed = profile.categories.first()
                    profile.categories.remove(removed)
                profile.categories.add(category)
        except:
            pass


        
    questionCategories = question.categories.all()
    if request.GET.get('request_type') == 'ajax':
        # just use this place to return the json response
        print("Python just comes at you like motherfucker!")
        return JsonResponse({"categories":[x.title for x in questionCategories],
                            "category_count": question.categories.count(),})

    context= {
        'page_obj': categories,
        'objCategories' : questionCategories,
        'question': question,
        'obj_type' : 'question',
        'q_id' : q_id,

    }
    # question:new-question

    return render(request, 'quiz/categoryCreate.html', context)





@login_required(redirect_field_name='next' ,login_url='account_login')
def CategoryRemove(request, question_id):
    question_id = question_id.split('-')
    if question_id[0] == 'trueOrFalse':
        question = TrueOrFalseQuestion.objects.prefetch_related("categories").get(id=question_id[1])
    elif question_id[0] == 'fourChoices':
        question = FourChoicesQuestion.objects.prefetch_related("categories").get(id=question_id[1])

    category = request.GET.get('removedCategory')
    category = Category.objects.get(title=category)
    question.categories.remove(category)
    print('category removed')
    return JsonResponse({"categories":[x.title for x in question.categories.all()],
                        "category_count": question.categories.count(),})




"""
Add all the documentation here
"""
@login_required(redirect_field_name='next' ,login_url='account_login')
def FourChoicesQuestionUpdate(request, question_id):
    user = request.user

    # question = get_object_or_404(FourChoicesQuestion, id=question_id)
    question = FourChoicesQuestion.objects.select_related('user').get(id=question_id)
    if not user == question.user:
        return HttpResponseForbidden()
    fourChoicesForm = NewFourChoicesQuestionForm(instance=question)
    if request.method == 'POST':
        form = NewFourChoicesQuestionForm(request.POST or None, instance=question)
        if form.is_valid():
            form.save()

            return redirect('question:category-create', question_id=f'fourChoices-{question.id}')

    
    context= {
        'fourChoicesForm': fourChoicesForm,
    }

    return render(request, 'question/fourChoicesQuestionCreate.html', context)


@login_required(redirect_field_name='next' ,login_url='account_login')
def TrueOrFalseQuestionUpdate(request, question_id):
    user = request.user
    question = TrueOrFalseQuestion.objects.get(id=question_id)
    if not user == question.user:
        return HttpResponseForbidden()
    trueOrFalseForm = NewTrueOrFalseQuestionForm(instance=question)
    if request.method == 'POST':
        form = NewTrueOrFalseQuestionForm(request.POST or None, instance=question)
        if form.is_valid():
            form.save()
        

            return redirect('question:category-create', question_id=f'trueOrFalse-{question.id}')

    
    context= {
        'trueOrFalseForm': trueOrFalseForm,
    }

    return render(request, 'question/trueOrFalseQuestionCreate.html', context)




@login_required(redirect_field_name='next' ,login_url='account_login')
def DeleteQuestion(request,question_form, question_id):
    user =request.user
    if question_form == 'fourChoices':
        question = FourChoicesQuestion.objects.select_related('user').get(id=question_id)
    elif question_form == 'trueOrFalse':
        question = TrueOrFalseQuestion.objects.select_related('user').get(id=question_id)
    if request.method == 'POST':
        if question.user == user:
            question.is_active = False
            question.save()
            # question.delete()
            return HttpResponse('Deleted!')
        else:
            return HttpResponseForbidden()

    context={
        'obj': question,
    }

    return render(request, 'question/delete.html', context)




"""
Each question will be submitted here
value="{{question.form}}|{{question.id}}|answer1"
"""
def SubmitQuestion(request):

    try:
        qtype = request.POST.get('questionType')
        creator = request.POST.get('creator')
        answer = request.POST.get('answer')
        if not answer:
            messages.error(request, _("You didn't provide any anwser"))
            if creator:
                response = redirect(request.META['HTTP_REFERER'])
                response['Location'] += f"?creator={creator}"
                return response
            return redirect(request.META['HTTP_REFERER'])


        if answer is None and qtype == 'following':
            if creator:

                response = redirect(request.META['HTTP_REFERER'])
                response['Location'] += f"?creator={creator}"
                return response
            return redirect('question:following-questions')
        elif answer is None and qtype == 'oldTownRoad':
            if creator:

                response = redirect(request.META['HTTP_REFERER'])
                response['Location'] += f"?creator={creator}"
                return response
            return redirect('question:answer-question')
        user = request.user
        if user.is_authenticated:

            profile = Profile.objects.select_related("user").prefetch_related("fourChoicesQuestionsTaken", "trueOrFalseQuestionsTaken",
             "fourChoicesQuestionsMissed", "trueOrFalseQuestionsMissed", "trueOrFalseQuestionsWareHouse",
              "fourChoicesQuestionsWareHouse").get(user=user)

        if request.method == 'POST':


            if user.is_authenticated:
                # streak = Streak.objects.get(profile=profile)
                profile.questionAttempts += 1
            combination = tuple(answer.split('-'))

            if combination[0] == 'fourChoicesQuestion':
                question = FourChoicesQuestion.objects.prefetch_related("categories").select_related("user").get(id=combination[1])
                pos = combination[2]
                question.attempts += 1
                    
                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1
                elif pos == 'answer3':
                    question.answer3NumberOfTimesTaken += 1
                elif pos == 'answer4':
                    question.answer4NumberOfTimesTaken += 1


                question.save()


                for category in question.categories.all():
                    category.question_number_of_times_taken += 1
                    category.save()
                    
                if question.correct == pos:



                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)

                    question.save()
                    if user.is_authenticated:
                        profile.fourChoicesQuestionsWareHouse.add(question)
                        if profile.fourChoicesQuestionsTaken.all().count() > 999:
                            removed = profile.fourChoicesQuestionsTaken.first()
                            profile.fourChoicesQuestionsTaken.remove(removed)
                        profile.fourChoicesQuestionsTaken.add(question)
                            
                        if profile.user != question.user:
                            # streak.validateStreak()
                            # streak.save()
                            """
                            This is a celery task
                            """
                            # StreakValidator.delay(profile, 1)


                            value = round((2 - question.avgScore/100) * 2, 2)
                            profile.coins += value
                            profile.questionAvgScore = decimal.Decimal(round(((profile.questionAvgScore * (profile.questionAttempts - 1)) + 100) / profile.questionAttempts ,1))
                            
                            profile.save()
                            """
                            This is a celery tasks
                            don't remove the previous task ooo because it is different from this celery task
                            """
                            # CoinsTransaction.delay(user, value)




                            if question.avgScore >= 50:
                                creator = Profile.objects.get(user=question.user)
                                creator.coins += decimal.Decimal(0.10)
                                creator.save()
                                # CreatorCoins.delay(creator.user, value)
                            messages.success(request, _(f"You've received {value} coins"))

                    messages.success(request, _('CORRECT!'))
                    
                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)
                    question.save()
                    if user.is_authenticated:
                        profile.fourChoicesQuestionsWareHouse.add(question)
                        
                        profile.coins -= 1
                        profile.questionAvgScore = decimal.Decimal(round((profile.questionAvgScore * (profile.questionAttempts - 1)) / profile.questionAttempts ,1))
                        if profile.fourChoicesQuestionsMissed.all().count() > 999:
                            removed = profile.fourChoicesQuestionsMissed.first()
                            profile.fourChoicesQuestionsMissed.remove(removed)
                        profile.fourChoicesQuestionsMissed.add(question)
                        profile.save()

                        messages.warning(request, _("You've lost 1 coin"))
                    messages.error(request, _('WRONG!'))
                    if creator:
                        response = redirect('question:correction', question_form=combination[0], question_id=combination[1], qtype=qtype, answer=pos)
                        response['Location'] += f"?creator={creator}"
                        return response

                    return redirect('question:correction', question_form=combination[0], question_id=combination[1], qtype=qtype, answer=pos)



            elif combination[0] == 'trueOrFalseQuestion':
                question = TrueOrFalseQuestion.objects.prefetch_related("categories").select_related("user").get(id=combination[1])
                pos = combination[2]
                question.attempts += 1
                    
                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1


                question.save()

                for category in question.categories.all():
                    category.question_number_of_times_taken += 1
                    category.save()

                
                answer = question.getAnswer(pos)

                if question.correct == answer:

                    

                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)
                    question.save()
                    if user.is_authenticated:
                        profile.trueOrFalseQuestionsWareHouse.add(question)
                        
                        if profile.trueOrFalseQuestionsTaken.all().count() > 999:
                            removed = profile.trueOrFalseQuestionsTaken.first()
                            profile.trueOrFalseQuestionsTaken.remove(removed)
                        profile.trueOrFalseQuestionsTaken.add(question)
                            
                        if profile.user != question.user:
                            # streak.validateStreak(1)
                            # streak.save()
                            """
                            This is a celery task
                            """

                            # StreakValidator.delay(profile, 1)



                            value = (2 - question.avgScore) * 2
                            profile.coins += value
                            profile.questionAvgScore = decimal.Decimal(round(((profile.questionAvgScore * (profile.questionAttempts - 1)) + 100) / profile.questionAttempts ,1))
                            
                            profile.save()
                            """
                            This is a celery tasks
                            don't remove the previous task ooo because it is different from this celery task
                            """
                            # CoinsTransaction.delay(user, value)



                            if question.avgScore >= 50:
                                creator = Profile.objects.get(user=question.user)

                                creator.coins += decimal.Decimal(0.10)
                                creator.save()
                                # CreatorCoins.delay(creator.user, value)
                            messages.success(request, _(f"You've received {value} coins"))

                    messages.success(request, _('CORRECT!'))
                    
                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)
                    question.save()

                    if user.is_authenticated:
                        profile.trueOrFalseQuestionsWareHouse.add(question)

                        profile.coins -= 1
                        if profile.trueOrFalseQuestionsMissed.all().count() > 999:
                            removed = profile.trueOrFalseQuestionsMissed.first()
                            profile.trueOrFalseQuestionsMissed.remove(removed)
                        profile.trueOrFalseQuestionsMissed.add(question)
                        profile.questionAvgScore = decimal.Decimal(round((profile.questionAvgScore * (profile.questionAttempts - 1)) / profile.questionAttempts ,1))
                        profile.save()
                        messages.warning(request, _("You've lost 1 coin"))
                    messages.error(request, _('WRONG!'))
                    if creator:
                        response = redirect('question:correction', question_form=combination[0], question_id=combination[1], qtype=qtype, answer=pos)
                        response['Location'] += f"?creator={creator}"
                        return response
                    return redirect('question:correction', question_form=combination[0], question_id=combination[1], qtype=qtype, answer=pos)

    except:
        pass
    if qtype == 'OldTownRoad' and creator != None:
        response = redirect('question:answer-question')
        response['Location'] += f"?creator={creator}"
        return response
    elif qtype == 'OldTownRoad' and creator == None:
        return redirect('question:answer-question')
    elif qtype == 'Following':
        return redirect('question:following-questions')

    HttpResponse('An error occurred!')



"""
Make the sql query of the page better by using
category.trueOrFalseQuestions.filter(lookup).exclude(lookdown) :)
"""
def QuizGenerator(request):
    user = request.user
    if request.method == "GET":
        if user.is_authenticated:

            profile = Profile.objects.prefetch_related('categories').get(user=user)

            categories = profile.categories.all().order_by('title')
        else:
            categories = Category.objects.all().order_by('quiz_number_of_times_taken')[:25]
        form = QuizGeneratorForm()

    if request.method == 'POST':
        profile = None
        if user.is_authenticated:
            profile = Profile.objects.prefetch_related('categories', 'trueOrFalseQuestionsTaken', 'trueOrFalseQuestionsMissed', 'fourChoicesQuestionsTaken', 'fourChoicesQuestionsMissed').get(user=user)

        try:
            form = QuizGeneratorForm(request.POST)

            if form.is_valid():
                duration_in_minutes = int(form.cleaned_data.get('duration_in_minutes')) * 60
                number_of_questions = form.cleaned_data.get('number_of_questions')
                categories = request.POST.getlist('categories')
                trueOrFalseQuestions = TrueOrFalseQuestion.objects.none()
                fourChoicesQuestions = FourChoicesQuestion.objects.none()
                if user.is_authenticated:
                    age = profile.get_user_age
                else:
                    age = 15
                for category in categories:
                    lookup = Q(is_active=True) & (Q(categories__title=category, solution_quality__gte=0, age_from__lte=age, age_to__gte=age))
                    trueOrFalseQuestions |= TrueOrFalseQuestion.objects.filter(lookup).distinct()[:1000]
                    fourChoicesQuestions |= FourChoicesQuestion.objects.filter(lookup).distinct()[:1000]
                trueOrFalseQuestions = trueOrFalseQuestions.distinct()
                fourChoicesQuestions = fourChoicesQuestions.distinct()


                trueOrFalseQuestionsTaken = profile.trueOrFalseQuestionsTaken.all()
                trueOrFalseQuestionsMissed = profile.trueOrFalseQuestionsMissed.all()
                fourChoicesQuestionsTaken = profile.fourChoicesQuestionsTaken.all()
                fourChoicesQuestionsMissed = profile.fourChoicesQuestionsMissed.all()
                questionsList = [*trueOrFalseQuestionsTaken, *trueOrFalseQuestionsMissed, *fourChoicesQuestionsTaken, *fourChoicesQuestionsMissed]

                questionSet = list((*trueOrFalseQuestions, *fourChoicesQuestions))



            

                questions = []
                i = 0
                while len(questions) < number_of_questions and len(questionSet) > 0:
                    question = randomChoice(questionSet)
                    questionSet.remove(question)
                    if (question not in questions) and (question not in questionsList):
                        questions.append(tuple((i, question)))
                        i += 1

                
                # questions = randomQuestions(questionSet, number_of_questions)
                questionLength = len(questions)
                if questionLength < number_of_questions:
                    messages.info(request, _('The questions are insufficient!'))

                request.session['duration'] = duration_in_minutes
                request.session['questionLength'] = questionLength
                sessionQuestions = []
                for question in questions:
                    
                    q = tuple((question[0], tuple((question[1].form, question[1].id))))
                    sessionQuestions.append(q)
                request.session['questions'] = sessionQuestions
                

                context = {
                'questions': questions,
                'duration': duration_in_minutes,
                'questionLength': questionLength,
                'reAttempt': 'no',
                'type': 'reAttempt',
                }
            return render(request, 'question/quiz.html', context)

        except:
            messages.error(request, _('There are no questions available!'))
            return redirect('question:questions')
            

    context={
        'form': form,
        'categories': categories,
    }

    return render(request, 'question/quizGenerator.html', context)




def ReAttemptQuiz(request):
    if request.method == 'POST':

        questions = request.session['questions']
        duration = request.session['duration']
        questionLength = request.session['questionLength']
        sessionQuestions = []
        for question in questions:
            index = question[0]
            if question[1][0] == 'trueOrFalseQuestion':
                q = TrueOrFalseQuestion.objects.get(id=question[1][1])
            elif question[1][0] == 'fourChoicesQuestion':
                q = FourChoicesQuestion.objects.get(id=question[1][1])
            pack_question = tuple((index, q))
            sessionQuestions.append(pack_question)



        context = {
                'questions': sessionQuestions,
                'duration': duration,
                'questionLength': questionLength,
                'reAttempt': 'yes',
                'type': 'reAttempt',
        }
        return render(request, 'question/quiz.html', context)




@login_required(redirect_field_name='next' , login_url='account_login')
def PastQuestions(request):
    try:
        user = request.user
        profile = Profile.objects.prefetch_related('trueOrFalseQuestionsTaken', 'trueOrFalseQuestionsMissed', 'fourChoicesQuestionsTaken', 'fourChoicesQuestionsMissed').get(user=user)

        trueOrFalseQuestionsTaken = profile.trueOrFalseQuestionsTaken.filter(is_active=True, standalone=True)
        trueOrFalseQuestionsMissed = profile.trueOrFalseQuestionsMissed.filter(is_active=True, standalone=True)
        fourChoicesQuestionsTaken = profile.fourChoicesQuestionsTaken.filter(is_active=True, standalone=True)
        fourChoicesQuestionsMissed = profile.fourChoicesQuestionsMissed.filter(is_active=True, standalone=True)

        questionsList = [*trueOrFalseQuestionsTaken, *trueOrFalseQuestionsMissed, *fourChoicesQuestionsTaken, *fourChoicesQuestionsMissed]

        questions = []

        i = 0

        while (len(questions) < 10) and (len(questionsList) > 0):

            question = randomChoice(questionsList)
            questionsList.remove(question)
            if question not in questions:
                questions.append(tuple((i, question)))
                i += 1

        questionLength = len(questions)
        if questionLength < 10:
            messages.info(request, _('The questions are insufficient!'))


        duration = 0
        for question in questions:
            duration += question[1].duration_in_seconds
    except:
        messages.error(request, _('You don\'t have any past questions available!'))
        return redirect('question:questions')

    context = {
        'questions': questions,
        'duration': duration,
        'questionLength': questionLength,
        'type': 'pastQuestions',

    }
    return render(request, 'question/quiz.html', context)

    





def SubmitQuizGenerator(request, ref_code, *args, **kwargs):
    user = request.user
    if request.method == 'GET':
        if not user.is_authenticated:
            code = str(kwargs.get('ref_code'))
            # use ref_code directly instead of kwargs
            ReferralService(request, code)   
        return redirect('question:quiz-generator')

    
    if request.method == 'POST':
        if user.is_authenticated:
            profile = Profile.objects.select_related("user").prefetch_related("fourChoicesQuestionsTaken", "trueOrFalseQuestionsTaken", "fourChoicesQuestionsMissed", "trueOrFalseQuestionsMissed", "trueOrFalseQuestionsWareHouse", "fourChoicesQuestionsWareHouse").get(user=user)
            # streak = Streak.objects.get(profile=profile)
    
    
        score = 0
        
        answers = request.POST.getlist('answer')
        if not answers:
            messages.error(request, _("You didn't provide any anwser"))
            return redirect(request.META['HTTP_REFERER'])
        reAttempt = request.POST.get('reAttempt')
        questionLength = request.POST.get('questionLength')
        questionType = request.POST.get('type')

        questionsList = []
  
        for answer in answers:
            combination = tuple(answer.split('-'))
            
            if combination[0] == 'fourChoices':
                question = FourChoicesQuestion.objects.prefetch_related("categories").select_related("user").get(id=combination[1])
                pos = combination[2]

                question.attempts += 1

                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1
                elif pos == 'answer3':
                    question.answer3NumberOfTimesTaken += 1
                elif pos == 'answer4':
                    question.answer4NumberOfTimesTaken += 1



                question.save()

                for category in question.categories.all():
                    category.question_number_of_times_taken += 1
                    category.save()
                    
                answer = question.getAnswer(pos)
                questionsList.append((question, answer))
                if question.correct == combination[2]:
                    score += 1


                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)
                    question.save()
                    if user.is_authenticated:
                        profile.fourChoicesQuestionsWareHouse.add(question)
                        if (question.user != profile.user) and (questionType != 'pastQuestions'):
                            profile.questionAttempts += 1
                                                  
                            creator = Profile.objects.get(user=question.user)
                            profile.questionAvgScore = decimal.Decimal(round(((profile.questionAvgScore * (profile.questionAttempts - 1)) + 100) / profile.questionAttempts ,1))
                            profile.save()
                            if question.avgScore >= 50:
                                creator.coins += decimal.Decimal(0.10)
                                creator.save()
                                # CreatorCoins.delay(creator.user, value)


                            if profile.fourChoicesQuestionsTaken.all().count() > 999:
                                removed = profile.fourChoicesQuestionsTaken.first()
                                profile.fourChoicesQuestionsTaken.remove(removed)
                            profile.fourChoicesQuestionsTaken.add(question)
                          





                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)
                    question.save()
                    if user.is_authenticated:
                        
                        profile.fourChoicesQuestionsWareHouse.add(question)
                        if question.user != profile.user:
                            profile.questionAttempts += 1
                            profile.questionAvgScore = decimal.Decimal(round((profile.questionAvgScore * (profile.questionAttempts - 1)) / profile.questionAttempts ,1))


                        if profile.fourChoicesQuestionsMissed.all().count() > 999:
                            removed = profile.fourChoicesQuestionsMissed.first()
                            profile.fourChoicesQuestionsMissed.remove(removed)
                        profile.fourChoicesQuestionsMissed.add(question)
                        

                    
            elif combination[0] == 'trueOrFalse':
                question = TrueOrFalseQuestion.objects.prefetch_related("categories").select_related("user").get(id=combination[1])
                pos = combination[2]

                question.attempts += 1

                if pos == 'answer1':
                    question.answer1NumberOfTimesTaken += 1
                elif pos == 'answer2':
                    question.answer2NumberOfTimesTaken += 1


                question.save()

                for category in question.categories.all():
                    category.question_number_of_times_taken += 1
                    category.save()
                    
                answer = question.getAnswer(combination[2])
                questionsList.append((question, answer))
                if question.correct == answer:
                    score += 1
                    question.avgScore = round(((question.avgScore *(question.attempts - 1) + 100) / question.attempts), 1)
                    question.save()
                    if user.is_authenticated:
                        profile.trueOrFalseQuestionsWareHouse.add(question)
                    
                        if (question.user != profile.user) and (questionType != 'pastQuestions'):
                            profile.questionAttempts += 1
                                                  
                            creator = Profile.objects.get(user=question.user)
                            profile.questionAvgScore = decimal.Decimal(round(((profile.questionAvgScore * (profile.questionAttempts - 1)) + 100) / profile.questionAttempts ,1))
                            profile.save()
                            if question.avgScore >= 50:
                                creator.coins += decimal.Decimal(0.10)
                                creator.save()
                                # CreatorCoins.delay(creator.user, value)


                            if profile.trueOrFalseQuestionsTaken.all().count() > 999:
                                removed = profile.trueOrFalseQuestionsTaken.first()
                                profile.trueOrFalseQuestionsTaken.remove(removed)
                            profile.trueOrFalseQuestionsTaken.add(question)
                            





                else:
                    question.avgScore = round((question.avgScore *(question.attempts - 1) / question.attempts), 1)
                    question.save()
                    if user.is_authenticated:
                        profile.trueOrFalseQuestionsWareHouse.add(question)
                        if question.user != profile.user:
                            profile.questionAttempts += 1
                            profile.questionAvgScore = decimal.Decimal(round((profile.questionAvgScore * (profile.questionAttempts - 1)) / profile.questionAttempts ,1))


                        if profile.trueOrFalseQuestionsMissed.all().count() > 999:
                                removed = profile.trueOrFalseQuestionsMissed.first()
                                profile.trueOrFalseQuestionsMissed.remove(removed)
                        profile.trueOrFalseQuestionsMissed.add(question)
                   


        total_score = int(questionLength)
        user_score = score
        user_avg_score = (user_score/total_score) * 100

        if user.is_authenticated:
            try:
                """
                Check if user is not quiz.user
                This is a celery task!
                """
                # StreakValidator.delay(profile, user_score)
                if user_avg_score > 50 and reAttempt == 'no':
                    value = user_score / 2
                    profile.coins += decimal.Decimal(value)
                    profile.save()
                    messages.success(request, _(f"You've won {value} coins!"))
                    """
                    This is a celery tasks
                    don't remove the previous task ooo because it is different from this celery task
                    """
                    # CoinsTransaction.delay(user, value)

            except ZeroDivisionError:
                pass
                messages.error(request, _("You didn't answer any question."))
                # return redirect('quiz:take-quiz', quiz_id = quiz.id)
        

        attempt_report = _(f"You answered {len(answers)} out of {questionLength} questions")
                   
        context = {
            'user_score': user_score,
            'user_avg_score': user_avg_score,
            'total_score': total_score,
            'questionsList': questionsList,
            'attempt_report': attempt_report,
            'questionLength': questionLength,
            'type': questionType,
            'postAd' : getAd('submit'),
            'page': 'submit',
        }

        
    return render(request, 'question/submitQuiz.html', context)







@login_required(redirect_field_name='next' ,login_url='account_login')
def SolutionQuality(request, question_form, question_id):
    user = request.user
    if user.is_authenticated:

        if question_form == 'fourChoices':
            question = FourChoicesQuestion.objects.prefetch_related('solution_validators').get(id=question_id)
        elif question_form == 'trueOrFalse':
            question = TrueOrFalseQuestion.objects.prefetch_related('solution_validators').get(id=question_id)

        quality = request.GET.get('quality')

        if quality == 'Yes':
            question.solution_quality += 1
            question.solution_validators.add(user)

        elif quality == 'No':
            question.solution_quality -= 1
            question.solution_validators.add(user)
        
        question.save()

    return HttpResponse('Modified Solution Quality!')



def TestQuestion(request):
    question1 = FourChoicesQuestion.objects.values("id", "user", "form", "question", "answer1", "answer2", "answer3", "answer4", "solution", "duration_in_seconds", "attempts", "avgScore")

    question2 = TrueOrFalseQuestion.objects.values("id", "user", "form", "question", "answer1", "answer2", "solution", "duration_in_seconds", "attempts", "avgScore")

    questions = [*question1, *question2]
    # print(questions)
    context = {
        'questions': questions,
    }
    return render(request, 'question/testquestion.html', context)







def TCorrectionView(request, question_form, question_id, answer):
    if question_form == 'fourChoicesQuestion':
        question = FourChoicesQuestion.objects.get(id=question_id)
        # print(question_form)
    elif question_form == 'trueOrFalseQuestion':
        question = TrueOrFalseQuestion.objects.get(id=question_id)
        # print(question_form)


    answer = question.getAnswer(answer)
    

    context={
        'question': question,
        'answer': answer,
    }

    return render(request, 'question/correction.html', context)

 