from django.urls import path
from . import views, api_views



app_name = 'room'
urlpatterns = [
    # add a slug field to the room
    path('<int:room_id>/<slug:slug>', views.StudyRoomPage.as_view(), name='room'),

    path('quiz/<int:room_id>', views.StudyRoomQuizList.as_view(), name='room-quiz'),
    path('question/<int:room_id>', views.RoomQuestions.as_view(), name='room-question'),
    path('four-choices-question/<int:room_id>', views.RoomFourChoicesQuestions.as_view(), name='room-four-choices-questions'),
    path('true-or-false-question/<int:room_id>', views.RoomTrueOrFalseQuestions.as_view(), name='room-true-or-false-questions'),
    #api view
    path('study-room', api_views.StudyRoomList.as_view(), name='room-list'),
    # path('<int:pk>/<slug:slug>', api_views.StudyRoomDetail.as_view(), name='room-detail'),
]