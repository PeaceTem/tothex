from django.db import models
from django.contrib.auth.models import User
from category.models import Category
# Create your models here.


class Book(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
        )
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(
        upload_to='images/books/thumbnails/',
        null=True
        )
    book = models.FileField(upload_to='books/')
    categories = models.ManyToManyField(
        Category,
        related_name='books'
        )
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title}"

