from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.utils import timezone
import pytz

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



# from question.models import TrueOrFalseQuestion, FourChoicesQuestion

from category.models import Category

from PIL import Image

from random import shuffle


from .managers import QuizManager


from .services import stringCleaningService

# Create your models here.

"""
Add the documentation to all the objects in the file.
This attempt is just for clarification in the process of making the whole app.

Control the redirect of tothex.org to tothex.org/quiz/
Create a QuizTemplate that all other types of quiz, like draft and scheduled, will inherit from.
Add the solution field to questions from the beginning of everything as part of the field of the different questions presented here.
Delete all the migrations files and dbsqlite3

Use Try, Except Block extensively in your views.
"""

"""
Users have the option to choose an answer from four different options
The index field is just the for ordering the questions in quiz 
The duration is in sec

Use Try except block thoroughly
# """



class Quiz(models.Model):

    DURATION_CHOICES = zip( range(1,61), range(1,61) )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(max_length=1000, verbose_name=_('Description'))
    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    when = models.CharField(max_length=200, null=True, blank=True)
    # fourChoicesQuestions = models.ManyToManyField(FourChoicesQuestion, related_name='fourChoicesQuestions',
        # related_query_name='fourChoicesQuestions' , blank=True)
    # trueOrFalseQuestions = models.ManyToManyField(TrueOrFalseQuestion, related_name='trueOrFalseQuestions',
        # related_query_name='trueOrFalseQuestions', blank=True)

    lastQuestionIndex = models.PositiveSmallIntegerField(default=0)
    questionLength = models.PositiveSmallIntegerField(default=0)
    totalScore = models.PositiveSmallIntegerField(default=0)
    shuffleQuestions = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    public = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True,
        related_name='categories', related_query_name='categories')
    duration = models.PositiveSmallIntegerField(default=0)
    get_duration = models.CharField(max_length=200, null=True, blank=True)
    solution_quality = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    likeCount = models.PositiveIntegerField(default=0)
    solution_validators = models.ManyToManyField(User,  blank=True, related_name='quiz_solution_validators')
    age_from = models.PositiveSmallIntegerField(null=True, verbose_name=_('Minimum Age Of Quiz Takers'))
    age_to = models.PositiveSmallIntegerField(null=True, verbose_name=_('Maximum Age Of Quiz Takers'))
    relevance = models.IntegerField(default=0)

    objects = QuizManager()





    def save(self, *args, **kwargs):
        
        dt = (self.date)
        dt_updated = (self.date_updated)
        if dt and dt_updated:
            # add the length of solution for questions
            rel = (self.questionLength * 5) + (self.attempts * 2) + (self.solution_quality * 10)
            
            self.relevance = rel

        self.get_duration = self.get_quiz_duration
        self.when = self.when_created 
        super().save(*args, **kwargs)


    def clean(self):
        a1 = self.age_from
        a2 = self.age_to
        if a1 is not None and a2 is not None and a1 > a2:
            raise ValidationError(_('minimum age should be less than or equal too maximum age'))

            if a2 > 65:
                raise ValidationError(_("The maximum age can be less than  or equal to 65"))

            if a2 - a1 > 4:
                raise ValidationError(_("The margin between the maximum and minimum age should not be more than 4 years"))
        
        self.description = stringCleaningService(self.description)

        super().clean()
    

    @property
    def get_quiz_duration(self):
        duration_in_sec = self.duration
        sec = duration_in_sec % 60
        minute = duration_in_sec // 60 
        if minute > 1 and sec > 1:
            return _(f"{minute}minutes:{sec}seconds")
        elif minute > 1 and sec <= 1:
            return _(f"{minute}minutes:{sec}second")
        elif minute <= 1 and sec > 1:
            return _(f"{minute}minute:{sec}seconds")
        elif minute <= 1 and sec <= 1:
            return _(f"{minute}minute:{sec}second")
        else:
            return None



    @property
    def last_update(self):
        days_length = date.today() - self.date_updated.date()
        days_length_shrink = str(days_length).split(',', 1)[0]
        return days_length_shrink


    @property
    def when_created(self):
        if not self.date:
            return timezone.now()
        days_length = timezone.now() - self.date
        days = days_length.days
        seconds = days_length.seconds
        if days > 0:
            try:
                days_length_shrink = int(days)

                if days_length_shrink > 364:
                    days_length_shrink = days_length_shrink // 365
                    if days_length_shrink < 2:
                        return f"{days_length_shrink} year"
                    return f"{days_length_shrink} years"
                elif days_length_shrink > 29:
                    days_length_shrink = days_length_shrink // 30
                    if days_length_shrink < 2:
                        return f"{days_length_shrink} month"
                    return f"{days_length_shrink} months"
                elif days_length_shrink > 6:
                    days_length_shrink = days_length_shrink // 7
                    if days_length_shrink < 2:
                        return f"{days_length_shrink} week"
                    return f"{days_length_shrink} weeks"
                if days_length_shrink < 2:
                        return f"{days_length_shrink} day"
                return f"{days_length_shrink} days"
            except:
                return f"0 days"
        elif seconds > 0:
            try:
                hours = seconds // 3600
                minutes = seconds // 60
                if hours > 0:
                    return f"{hours} hours"
                elif minutes > 0:
                    return f"{minutes} minutes"

                else:
                    return f"{seconds} seconds"
                    

            except:
                return f"0 seconds"
        return timezone.now()


    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Quizzes'

        
    def __str__(self):
        return f"{self.title}"





class QuizLink(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name='quizlink', editable=False)
    name = models.CharField(max_length=80, verbose_name=_('Name'))
    link = models.URLField(verbose_name=_('Link/URL'))
    description = models.TextField(max_length=200, verbose_name=_('Description'))
    ban = models.BooleanField(default=False)
    reportCount = models.PositiveSmallIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    reporters = models.ManyToManyField(User, blank=True)





class Attempter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempters')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempters')
    score = models.PositiveSmallIntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    timeTaken = models.PositiveSmallIntegerField(default=0)


    class Meta:
        ordering = ['-percentage', '-score', 'timeTaken']

    @property
    def get_percentage(self):
        return f"{self.percentage}%"


    @property
    def get_timetaken(self):
        TimeTaken = self.timeTaken
        minutesTaken = int(TimeTaken) // 60
        secondsTaken = int(TimeTaken) % 60

        timeTaken = f"{minutesTaken}min : {secondsTaken}sec."
        return timeTaken


    def __str__(self):
        return f"{self.user.username}"

    # check if the attempter has not been created before creating another instance of attempter



# class Person(models.Model):
#     name = CharField(max_length=100)
#     age = supply property




# class Author(models.Model):
#     person = supply the property


# class Book(models.Model):
#     name = CharField(max_length=100)

#     published_date = supply the property
#     # a book has many readers and may have many authors
#     readers = supply the property
#     authors = supply the property
#     category = supply field

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True, help_text="Each category is unique!")
#     # register by a person
#     registered_by = supply the field to this property of the object category.
#     date_created = supply the field to this property of the object category.




# class Library(models.Model):
#     name = models.CharField(max_length=100)
#     librarian = supply field
#     books = supply field

    # def save(self, *args, **kwargs):
    #     #use the pre_save signal to handle this task.
    #     # change this at property
    #     print('printing')

    #     if self.age_to is None and self.age_from is None:
    #         age = None
    #         try:
    #             age = self.user.profile.date_of_birth
    #             age = date.today() - age
    #             age = age.days // 365
    #             print(age)
    #             if age < 65:
    #                 print(age)
    #                 self.age_from = age - 2
                    
    #                 self.age_to = age
    #                 super().save(*args, **kwargs)
    #                 print('saved')
    #         except:
    #             pass
    #     super().save(*args, **kwargs)