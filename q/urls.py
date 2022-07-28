from django.urls import path
from . import views

app_name = 'qxa'


urlpatterns = [
    path('create-question', views.CreateQuestion.as_view(), name='create-question'),
    path('answer-question/<int:q_id>', views.CreateAnswer.as_view(), name='answer-question'),
    path('answers/reply/<int:a_id>', views.CreateReply.as_view(), name='create-reply'),

    
    path('', views.QuestionPage.as_view(), name='question-page'),
    path('answers/<slug:slug>', views.AnswerPage.as_view(), name='answer-page'),

]
