from django.contrib import admin
from .models import Quiz, QuizLink, Attempter

# Register your models here.
admin.site.register(Quiz)
admin.site.register(QuizLink)
admin.site.register(Attempter)
