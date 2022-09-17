from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.



"""
Add Search To This Part That Filter Results In Real-Time With JavaScript
Make This Design Of This Page Looks Like Google Search Results
How To:
    - Change Username
    - Change Password
    - Change Categories
    - Create Quiz
    - Add Categories To Quiz
    - Add Questions To Quiz
    - Create Questions
    - Rank High
    - Take Quiz
    - Edit Quiz
    - Delete Quiz
    - Edit Question
    - Delete Question
    - Edit Profile
    - Answer Question From A Particular User
    - What Is My Coven
    - What Is Bohemian Grove
    - What Is Old Town Road
"""


class HowTo(TemplateView):
    template_name='how_to/how_to.html'