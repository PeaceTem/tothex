from django.urls import path
from . import views

app_name = 'qxa'


urlpatterns = [
    path('create-question', views.CreateQuestion.as_view(), name='create-question'),
    path('answer-question/<int:q_id>', views.CreateAnswer.as_view(), name='answer-question'),
    path('answers/reply/<int:a_id>', views.CreateReply.as_view(), name='create-reply'),

    
    path('', views.QuestionPage.as_view(), name='question-page'),
    path('answers/<slug:slug>/<int:pk>', views.AnswerPage.as_view(), name='answer-page'),
    path('my-questions', views.MyQPage.as_view(), name='my-q'),
    # the global category list url
    path('category/list/', views.CategoryList.as_view(), name='category-list')


]
