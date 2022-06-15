from django.db import models
from django.contrib.auth.models import User
# Create your models here.






"""
Perform some calculations on the number of times the category has being taken.
and the relevance

Add the number of questions with this category
"""

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    relevance = models.IntegerField(default=0)
    number_of_quizzes = models.PositiveIntegerField(default=0)
    number_of_questions = models.PositiveIntegerField(default=0)
    # this represent the number of times the quizzes affiliated with this category were taken
    quiz_number_of_times_taken = models.PositiveIntegerField(default=0)
    question_number_of_times_taken = models.PositiveIntegerField(default=0)
    date_registered = models.DateTimeField(auto_now_add=True)
    #add images to this Also
    # add languages too.

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return f"{self.title}"

