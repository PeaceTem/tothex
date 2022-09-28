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
    path('category/list/', views.CategoryList.as_view(), name='category-list'),

    path('category-create/<str:q_id>/', views.CategoryCreate.as_view(), name='category-create'),
    path('category-remove/<str:q_id>/', views.CategoryRemove.as_view(), name='category-remove'),

    #upvote and downvote question and answer
    path('upvote-question/<int:q_id>', views.UpvoteQuestion.as_view(), name="upvote-question"),
    path('downvote-question/<int:q_id>', views.DownvoteQuestion.as_view(), name="downvote-question"),


    path('upvote-answer/<int:a_id>', views.UpvoteAnswer.as_view(), name="upvote-answer"),
    path('downvote-answer/<int:a_id>', views.DownvoteAnswer.as_view(), name="downvote-answer"),

]
