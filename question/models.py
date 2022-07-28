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
    DURATION_CHOICES = zip( range(15,181, 5), range(15,181, 5) )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fourchoicesquestions')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='fourChoicesQuestions')
    form = models.CharField(max_length=30, default='fourChoicesQuestion')
    index = models.PositiveSmallIntegerField(default=0)
    question = models.TextField(max_length=1000, verbose_name=_('Question'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    answer1 = models.CharField(max_length=200, verbose_name=_('First Option'))
    answer2 = models.CharField(max_length=200, verbose_name=_('Second Option'))
    answer3 = models.CharField(max_length=200, verbose_name=_('Third Option'))
    answer4 = models.CharField(max_length=200, verbose_name=_('Fourth Option'))
    correct = models.CharField(max_length=100, choices=ANSWER_CHOICES, verbose_name=_('Correct Option'))
    points = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, default=1)
    solution = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Solution'))
    duration_in_seconds = models.PositiveSmallIntegerField(choices=DURATION_CHOICES, default=30, verbose_name=_('Duration In Seconds'))
    categories = models.ManyToManyField(Category, related_name='FourChoicesQuestioncategories', blank=True)
    attempts = models.PositiveIntegerField(default=0)
    avgScore = models.FloatField(default=0.0)
    solution_quality = models.IntegerField(default=0)
    solution_validators = models.ManyToManyField(User,  blank=True, related_name='fourChoicesQuestion_solution_validators')
    answer1NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer2NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer3NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer4NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    shuffleAnswers = models.BooleanField(default=False, verbose_name=_('Shuffle The Answers'))
    standalone = models.BooleanField(default=True, verbose_name=_("Create as a standalone question too"))
    age_from = models.PositiveSmallIntegerField(null=True, verbose_name=_('Minimum Age Of Quiz Takers'))
    age_to = models.PositiveSmallIntegerField(null=True, verbose_name=_('Maximum Age Of Quiz Takers'))
    relevance = models.IntegerField(default=0)
    
    objects = FourChoicesQuestionManager()




    def clean(self):
        a1 = self.age_from
        a2 = self.age_to
        if a1 is not None and a2 is not None and a1 > a2:
            raise ValidationError(_('minimum age should be less than or equal too maximum age'))

            if a2 > 65:
                raise ValidationError(_("The maximum age can be less than  or equal to 65"))

            if a2 - a1 > 4:
                raise ValidationError(_("The margin between the maximum and minimum age should not be more than 4 years"))
        
        self.question = stringCleaningService(self.question)
        self.answer1 = stringCleaningService(self.answer1)
        self.answer2 = stringCleaningService(self.answer2)
        self.answer3 = stringCleaningService(self.answer3)
        self.answer4 = stringCleaningService(self.answer4)
        self.solution = stringCleaningService(self.solution)

        super().clean()
    

    def save(self, *args, **kwargs):
         
        dt = (self.date_created)
        dt_updated = (self.date_updated)
        if dt and dt_updated and self.solution:
            rel = (len(self.solution.split()) * 2) + (len(self.question.split()) * 3) + (self.attempts * 5) + (self.solution_quality * 100)
            
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
        ('answer1', _('True')),
        ('answer2', _('False')),
    )


    DURATION_CHOICES = zip(range(15,181, 5), range(15,181, 5))
    SCORE_CHOICES = zip( range(5,0, -1), range(5,0, -1) )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trueOrFalseQuestions')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='trueOrFalseQuestions')

    form = models.CharField(max_length=20, default='trueOrFalseQuestion')
    index = models.PositiveSmallIntegerField(default=0)
    question = models.TextField(max_length=1000, verbose_name=_('Question'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    answer1 = models.CharField(max_length=20, default=_('True'))
    answer2 = models.CharField(max_length=20, default=_('False'))
    correct = models.CharField(max_length=100, choices=ANSWER_CHOICES, verbose_name=_('Correct Option'))
    points = models.PositiveSmallIntegerField(choices=SCORE_CHOICES, default=1, verbose_name=_('Points'))

    solution = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Solution'))
    duration_in_seconds = models.PositiveSmallIntegerField(choices=DURATION_CHOICES, default=20, verbose_name=_('Duration In Seconds'))
    categories = models.ManyToManyField(Category, related_name='trueOrFalseQuestioncategories', blank=True)
    attempts = models.PositiveIntegerField(default=0)
    avgScore = models.FloatField(default=0.0)
    solution_quality = models.IntegerField(default=0)
    solution_validators = models.ManyToManyField(User, related_name='trueOrFalse_solution_validators', blank=True)
    answer1NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    answer2NumberOfTimesTaken = models.PositiveIntegerField(default=0)
    standalone = models.BooleanField(default=True, verbose_name=_("Create as a standalone question too"))
    age_from = models.PositiveSmallIntegerField(null=True, verbose_name=_('Minimum Age Of Quiz Takers'))
    age_to = models.PositiveSmallIntegerField(null=True, verbose_name=_('Maximum Age Of Quiz Takers'))
    relevance = models.IntegerField(default=0)
    
  

    objects = TrueOrFalseQuestionManager()



    def clean(self):
        a1 = self.age_from
        a2 = self.age_to
        if a1 is not None and a2 is not None and a1 > a2:
            raise ValidationError(_('minimum age should be less than or equal too maximum age'))

            if a2 > 65:
                raise ValidationError(_("The maximum age can be less than  or equal to 65"))
            if a2 - a1 > 4:
                raise ValidationError(_("The margin between the maximum and minimum age should not be more than 4 years"))
        
        self.question = stringCleaningService(self.question)
        
        self.solution = stringCleaningService(self.solution)

        super().clean()
    




    def save(self, *args, **kwargs):
         
        dt = (self.date_created)
        dt_updated = (self.date_updated)
        if dt and dt_updated and self.solution:
            rel = (len(self.solution.split()) * 2) + (len(self.question.split()) * 3) + (self.attempts * 5) + (self.solution_quality * 100)
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
        else:
            return None




    def __str__(self):
        return f"{self.question}"






