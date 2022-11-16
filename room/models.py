from django.db import models
from django.contrib.auth.models import User
from quiz.models import Quiz
from question.models import FourChoicesQuestion, TrueOrFalseQuestion
from q.models import Q as Question
from django.utils.text import slugify

# Create your models here.


class StudyRoom(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='rooms')
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.name}"

# add a signal that creates announcement whenever a study room is created




class Announcement(models.Model):
    room = models.OneToOneField(StudyRoom, on_delete=models.CASCADE, related_name='announcement')
    announcement = models.CharField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return f"{self.room}"
        

class RoomMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_member')
    room = models.ForeignKey(StudyRoom, null=True, on_delete=models.CASCADE, related_name='members')
    date_joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}"


class RoomQuiz(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes_sponsored')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='rooms')
    room = models.ForeignKey(StudyRoom, null=True, on_delete=models.CASCADE, related_name='quizzes')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quiz}"


class RoomQuestion(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions_sponsored')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='rooms')
    room = models.ForeignKey(StudyRoom, null=True, on_delete=models.CASCADE, related_name='questions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question}"




class RoomFourChoicesQuestion(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fourChoicesQuestion_sponsored')
    fourChoicesQuestion = models.ForeignKey(FourChoicesQuestion, on_delete=models.CASCADE, related_name='rooms')
    room = models.ForeignKey(StudyRoom, null=True, on_delete=models.CASCADE, related_name='fourChoicesQuestions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fourChoicesQuestion}"





class RoomTrueOrFalseQuestion(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trueOrFalseQuestion_sponsored')
    trueOrFalseQuestion = models.ForeignKey(TrueOrFalseQuestion, on_delete=models.CASCADE, related_name='rooms')
    room = models.ForeignKey(StudyRoom, null=True, on_delete=models.CASCADE, related_name='trueOrFalseQuestions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trueOrFalseQuestion}"



