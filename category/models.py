from tabnanny import verbose
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
    quiz_number_of_times_taken = models.PositiveIntegerField(default=0)
    question_number_of_times_taken = models.PositiveIntegerField(default=0)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return f"{self.title}"


class MyCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myCategories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='users_categories')
    def __str__(self):
        return f"{self.category}"


    class Meta:
        verbose_name_plural = 'MyCategories'


    def save(self, **kwargs):
        # print(kwargs)
        user = self.user
        # print(user)
        myCategories = user.myCategories.all()
        # print(myCategories)
        if str(self.category) in [str(c) for c in myCategories]:
            # print('This category all exist for this user!')
            return None
        # print('The category is successfully created')
        super().save(**kwargs)
