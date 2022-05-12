from django.urls import path


from . import views



app_name = 'quiz'

 
urlpatterns = [
    path('custom/', views.CustomCheckbox, name='custom'),
    path('', views.QuizList, name='quizzes'),
    path('following-quizzes/', views.FollowerQuizList, name='following-quizzes'),
    path('my-quizzes/', views.MyQuizList, name='my-quizzes'),
    path('quizzes-taken/', views.QuizTakenList, name='quizTaken'),
    path('favorites/', views.FavoriteQuizList, name='favorites'),


    path('detail/<str:quiz_id>/<str:ref_code>', views.QuizDetail, name='quiz-detail'),
    path('create-quiz/', views.QuizCreate, name='quiz-create'),
    path('create/', views.CreateObject, name='object-create'),
    path('edit-quiz/<str:quiz_id>/', views.QuizUpdate, name='quiz-update'),
    path('delete-quiz/<quiz_id>/', views.DeleteQuiz, name='delete-quiz'),
    path('delete-question/<str:quiz_id>/<str:question_form>/<str:question_id>/', views.DeleteQuestion, name='delete-question'),

    # quiz link
    path('link/report/', views.ReportLink.as_view(), name='report-link'),
    path('link/<str:quiz_id>/', views.QuizLinkCreate.as_view(), name='create-quiz-link'),
    path('link/<str:quizlink_id>/click/', views.QuizLinkClickCounter.as_view(), name='quiz-link-click-counter'),

    # random quiz picker
    path('random/', views.RandomQuizPicker.as_view(), name='random-quiz-picker'),

    # category
    path('category/<str:category>/', views.CategoryQuizList, name='category-quiz'),



    #like post
    path('like/', views.PostLike, name ='post-like'),

    #category
    path('create_category/<str:quiz_id>/', views.CategoryCreate, name='category-create'),

    #question
    path('<str:quiz_id>/new-question/', views.QuestionCreate, name='new-question'),

    path('<str:quiz_id>/create-question/four-choices/', views.FourChoicesQuestionCreate, name='fourChoicesQuestion'),
    path('<str:quiz_id>/edit-question/four-choices/<str:question_id>/', views.FourChoicesQuestionUpdate, name='edit-fourChoicesQuestion'),


    path('<str:quiz_id>/create-question/true-or-false/', views.TrueOrFalseQuestionCreate, name='trueOrFalseQuestion'),
    path('<str:quiz_id>/edit-question/true-or-false/<str:question_id>/', views.TrueOrFalseQuestionUpdate, name='edit-trueOrFalseQuestion'),
    #takequiz

    path('<str:quiz_id>/take/', views.TakeQuiz, name='take-quiz'),
    path('<str:quiz_id>/submit/<str:ref_code>', views.SubmitQuiz, name='submit-quiz'),
    path('solution-quality/<str:quiz_id>/', views.SolutionQuality, name='solution-quality'),

    #pdf generation
    path('<str:quiz_id>/pdf/', views.GeneratePDF.as_view(), name='quiz-pdf'),
]
# # from .views import (GeneratePDF, QuizList, QuizDetail, QuizCreate, QuizUpdate, DeleteQuiz, CategoryCreate, QuestionCreate,
# #  FourChoicesQuestionCreate, FourChoicesQuestionUpdate, TrueOrFalseQuestionCreate, TrueOrFalseQuestionUpdate, TakeQuiz, SubmitQuiz)