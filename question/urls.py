from django.urls import path


from . import views



app_name = 'question'


urlpatterns = [
    #question
    path('new-question/', views.QuestionCreate, name='new-question'),
    path('', views.Question, name='questions'),
    path('my-questions/', views.MyQuestionList, name='my-questions'),
    path('visitor-questions/<int:owner_id>/', views.VisitorView, name='visitor'),

    path('following-questions/', views.FollowingQuestion, name='following-questions'),


    path('create-question/four-choices/', views.FourChoicesQuestionCreate, name='fourChoicesQuestion'),
    path('edit-question/four-choices/<str:question_id>/', views.FourChoicesQuestionUpdate, name='edit-fourChoicesQuestion'),


    path('create-question/true-or-false/', views.TrueOrFalseQuestionCreate, name='trueOrFalseQuestion'),
    path('edit-question/true-or-false/<str:question_id>/', views.TrueOrFalseQuestionUpdate, name='edit-trueOrFalseQuestion'),

    path('category-create/<str:question_id>/', views.CategoryCreate, name='category-create'),
    path('category-remove/<str:question_id>/', views.CategoryRemove, name='category-remove'),


    path('question-delete/<str:question_form>/<str:question_id>/', views.DeleteQuestion, name='delete-question'),

    # answer question
    path('take/', views.AnswerQuestion, name='answer-question'),
    path('four-choices-question/<int:pk>/take', views.TakeFourChoicesQuestion.as_view(), name="take-four-choices-question"),
    path('true-or-false-question/<int:pk>/take', views.TakeTrueOrFalseQuestion.as_view(), name="take-true-or-false-question"),
    path('submit/', views.SubmitQuestion, name='submit-question'),
    path('correction/<str:question_form>/<str:question_id>/<str:qtype>/<str:answer>/', views.CorrectionView, name='correction'),
    




    path('quiz-generator/', views.QuizGenerator, name='quiz-generator'),
    path('quiz-submit/<str:ref_code>/', views.SubmitQuizGenerator, name='quiz-submit'),
    path('retake-quiz/', views.ReAttemptQuiz, name='retake-quiz'),
    path('solution_quality/<str:question_form>/<str:question_id>', views.SolutionQuality, name='solution-quality'),



    path('past-questions/', views.PastQuestions, name='past-questions'),


    # test

    path('test/', views.TestQuestion, name='test'),
]







