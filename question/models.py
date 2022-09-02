from django.db import models
from django.contrib.auth.models import User
from category.models import Category

from random import shuffle
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from datetime import date, datetime, time
from django.utils import timezone
from .managers import FourChoicesQuestionManager
from .managers import TrueOrFalseQuestionManager

from quiz.services import stringCleaningService


from quiz.models import Quiz
from ckeditor.fields import RichTextField

# Create your models here.
"""
User should be able to like this quiz
"""



class FourChoicesQuestion(models.Model):
    ANSWER_CHOICES = (
        ('answer1', _('First Option')),
        ('answer2', _('Second Option')),
        ('answer3', _('Third Option')),
        ('answer4', _('Fourth Option')),
    )

    SCORE_CHOICES = zip( range(5,0, -1), range(5,0, -1) )
    DURATION_CHOICES = zip( range(15,301, 5), range(15,301, 5) )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fourChoicesQuestions')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='fourChoicesQuestions')
    form = models.CharField(max_length=30, default='fourChoicesQuestion')
    index = models.PositiveSmallIntegerField(default=0)
    question = RichTextField(max_length=1000, verbose_name=_('Question'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    answer1 = models.CharField(max_length=200, verbose_name=_('First Option'))
    answer2 = models.CharField(max_length=200, verbose_name=_('Second Option'))
    answer3 = models.CharField(max_length=200, verbose_name=_('Third Option'))
    answer4 = models.CharField(max_length=200, verbose_name=_('Fourth Option'))
    correct = models.CharField(max_length=100, choices=ANSWER_CHOICES, verbose_name=_('Correct Option'))
    points = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, default=1)
    solution = RichTextField(max_length=1000, null=True, blank=True, verbose_name=_('Solution'))
    duration_in_seconds = models.PositiveSmallIntegerField(choices=DURATION_CHOICES, default=30, verbose_name=_('Duration In Seconds'))
    categories = models.ManyToManyField(Category, related_name='fourChoicesQuestions', blank=True)
    views = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    avgScore = models.FloatField(default=0.0)
    solution_quality = models.IntegerField(default=0)
    solution_validators = models.ManyToManyField(User,  blank=True, related_name='fourChoicesQuestion_solution_validators')
    answer1NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer2NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer3NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer4NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    shuffleAnswers = models.BooleanField(default=False, verbose_name=_('Shuffle The Answers'))
    standalone = models.BooleanField(default=True, verbose_name=_("Create as an OldTownRoad question too"))
    age_from = models.PositiveSmallIntegerField(default=11, verbose_name=_('Minimum Age Of Quiz Takers'))
    age_to = models.PositiveSmallIntegerField(default=65, verbose_name=_('Maximum Age Of Quiz Takers'))
    relevance = models.IntegerField(default=0)
    
    objects = FourChoicesQuestionManager()




    def clean(self):
        a1 = self.age_from
        a2 = self.age_to
        if a1 is not None and a2 is not None and a1 > a2:
            raise ValidationError(_('minimum age should be less than or equal too maximum age'))

        super().clean()
    

    def save(self, *args, **kwargs):
         
        dt = (self.date_created)
        dt_updated = (self.date_updated)
        if dt and dt_updated and self.solution:
            rel = (len(self.solution.split())) + (self.attempts * 2) + (self.solution_quality * 10)
            
            self.relevance = rel


        super().save(*args, **kwargs)



    @property
    def shuffle_answers(self):
        _newlist = [1,2,3,4]
        if self.shuffleAnswers:
            shuffle(_newlist)
        return _newlist

    @property
    def get_percentage_chosen_of_answer1(self):
        total_question_attempts = self.attempts
        _answer1 = self.answer1NumberOfTimesTaken
        result = round((_answer1/total_question_attempts) * 100,2)

        return f"{result}%"



    @property
    def get_percentage_chosen_of_answer2(self):
        total_question_attempts = self.attempts
        _answer2 = self.answer2NumberOfTimesTaken
        result = round((_answer2/total_question_attempts) * 100,2)

        return f"{result}%"



    @property
    def get_percentage_chosen_of_answer3(self):
        total_question_attempts = self.attempts
        _answer3 = self.answer3NumberOfTimesTaken
        result = round((_answer3/total_question_attempts) * 100,2)

        return f"{result}%"


    @property
    def get_percentage_chosen_of_answer4(self):
        total_question_attempts = self.attempts
        _answer4 = self.answer4NumberOfTimesTaken
        result = round((_answer4/total_question_attempts) * 100,2)

        return f"{result}%"





    @property
    def when_created(self):
        days_length = date.today() - self.date_created.date()
        print(days_length)
        
        try:
            days_length_shrink = str(days_length).split(',', 1)[0]
            days_length_shrink = days_length_shrink[:len(days_length_shrink) - 4]

            days_length_shrink = int(days_length_shrink)

            if days_length_shrink > 364:
                days_length_shrink = days_length_shrink // 365
                if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} year"
                return f"{str(days_length_shrink)} years"
            elif days_length_shrink > 29:
                days_length_shrink = days_length_shrink // 30
                if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} month"
                return f"{str(days_length_shrink)} months"
            elif days_length_shrink > 6:
                days_length_shrink = days_length_shrink // 7
                if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} week"
                return f"{str(days_length_shrink)} weeks"
            if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} day"
            return f"{str(days_length_shrink)} days"
        except:
            return f"0 days"


    def getAnswer(self, value, *args, **kwargs):
        if value == 'answer1':
            return self.answer1
        elif value == 'answer2':
            return self.answer2
        elif value == 'answer3':
            return self.answer3
        elif value == 'answer4':
            return self.answer4
        else:
            return None




    def __str__(self):
        return f"{self.question}"




class TrueOrFalseQuestion(models.Model):
    ANSWER_CHOICES = (
        ('True', _('True')),
        ('False', _('False')),
    )


    DURATION_CHOICES = zip(range(15,301, 5), range(15,301, 5))
    SCORE_CHOICES = zip( range(5,0, -1), range(5,0, -1) )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trueOrFalseQuestions')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='trueOrFalseQuestions')

    form = models.CharField(max_length=20, default='trueOrFalseQuestion')
    index = models.PositiveSmallIntegerField(default=0)
    question = RichTextField(max_length=1000, verbose_name=_('Question'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    answer1 = models.CharField(max_length=20, default='True')
    answer2 = models.CharField(max_length=20, default='False')
    correct = models.CharField(max_length=100, choices=ANSWER_CHOICES, verbose_name=_('Correct Option'))
    points = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, default=1, verbose_name=_('Points'))

    solution = RichTextField(max_length=1000, null=True, blank=True, verbose_name=_('Solution'))
    duration_in_seconds = models.PositiveSmallIntegerField(choices=DURATION_CHOICES, default=30, verbose_name=_('Duration In Seconds'))
    categories = models.ManyToManyField(Category, related_name='trueOrFalseQuestions', blank=True)
    views = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    avgScore = models.FloatField(default=0.0)
    solution_quality = models.IntegerField(default=0)
    solution_validators = models.ManyToManyField(User, related_name='trueOrFalse_solution_validators', blank=True)
    answer1NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer2NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    standalone = models.BooleanField(default=True, verbose_name=_("Create as a standalone question too"))
    age_from = models.PositiveSmallIntegerField(default=11, verbose_name=_('Minimum Age Of Quiz Takers'))
    age_to = models.PositiveSmallIntegerField(default=65, verbose_name=_('Maximum Age Of Quiz Takers'))
    relevance = models.IntegerField(default=0)
    
  

    objects = TrueOrFalseQuestionManager()



    def clean(self):
        a1 = self.age_from
        a2 = self.age_to
        if a1 is not None and a2 is not None and a1 > a2:
            raise ValidationError(_('minimum age should be less than or equal too maximum age'))

        super().clean()
    




    def save(self, *args, **kwargs):
         
        dt = (self.date_created)
        dt_updated = (self.date_updated)
        if dt and dt_updated and self.solution:
            rel = (len(self.solution.split())) + (self.attempts) + (self.solution_quality * 10)
            self.relevance = rel


        super().save(*args, **kwargs)





    @property
    def get_percentage_chosen_of_answer1(self):
        total_question_attempts = self.attempts
        _answer1 = self.answer1NumberOfTimesTaken
        result = round((_answer1/total_question_attempts) * 100,2)

        return f"{result}%"



    @property
    def get_percentage_chosen_of_answer2(self):
        total_question_attempts = self.attempts
        _answer2 = self.answer2NumberOfTimesTaken
        result = round((_answer2/total_question_attempts) * 100,2)

        return f"{result}%"





    @property
    def when_created(self):
        days_length = date.today() - self.date_created.date()
        
        try:
            days_length_shrink = str(days_length).split(',', 1)[0]
            days_length_shrink = days_length_shrink[:len(days_length_shrink) - 4]

            days_length_shrink = int(days_length_shrink)

            if days_length_shrink > 364:
                days_length_shrink = days_length_shrink // 365
                if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} year"
                return f"{str(days_length_shrink)} years"
            elif days_length_shrink > 29:
                days_length_shrink = days_length_shrink // 30
                if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} month"
                return f"{str(days_length_shrink)} months"
            elif days_length_shrink > 6:
                days_length_shrink = days_length_shrink // 7
                if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} week"
                return f"{str(days_length_shrink)} weeks"
            if days_length_shrink < 2:
                    return f"{str(days_length_shrink)} day"
            return f"{str(days_length_shrink)} days"
        except:
            return f"0 days"



    def getAnswer(self, value, *args, **kwargs):
        if value == 'answer1':
            return self.answer1
        elif value == 'answer2':
            return self.answer2
        else:
            return None




    def __str__(self):
        return f"{self.question}"


class TrueOrFalseAttempter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempted_true_or_false_question')
    question = models.ManyToManyField(TrueOrFalseQuestion, blank=True, related_name='attempters')
    timetaken = models.PositiveSmallIntegerField(null=True)
    correct = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.question}"



class FourChoicesAttempter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempted_four_choices_question')
    question = models.ManyToManyField(FourChoicesQuestion, blank=True, related_name='attempters')
    timetaken = models.PositiveSmallIntegerField(null=True)
    correct = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.question}"


