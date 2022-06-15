from django.shortcuts import render

# Create your views here.

from .models import Competition
from quiz.models import Quiz



"""
Create a get and post view
the number of beneficiaries will be added (3)
The Quiz that will be used will be added later, then the competition will be active (1)
The prize will be added (2)


A fixed percentage will be set, any user that crosses the threshold will be give a prize immediately

"""

# def CompetitionCreate(request, quiz_id):
#     quiz = Quiz.objects.get(id=quiz_id)

#     competition = Competition.objects.create(quiz=quiz)





#     pass