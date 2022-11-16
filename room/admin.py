from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(StudyRoom)
admin.site.register(Announcement)
admin.site.register(RoomMember)
admin.site.register(RoomQuiz)
admin.site.register(RoomQuestion)
admin.site.register(RoomFourChoicesQuestion)
admin.site.register(RoomTrueOrFalseQuestion)

