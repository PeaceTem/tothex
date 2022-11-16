from rest_framework import serializers
from .models import *
from core.serializers import UserSerializer
from quiz.serializers import QuizSerializer
from question.serializers import FourChoicesQuestionSerializer, TrueOrFalseQuestionSerializer
from q.serializers import QSerializer



class StudyRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True).data
    class Meta:
        model = StudyRoom
        fields = (
            'user',
            'name',
            'date_created',
            'date_updated'
            )
        depth = 1



class AnnouncementSerializer(serializers.ModelSerializer):
    room = StudyRoomSerializer(read_only=True).data
    class Meta:
        model = Announcement
        fields = (
            'room',
            'announcement'
        )
        depth = 1



class RoomMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True).data
    room = StudyRoomSerializer(read_only=True).data
    class Meta:
        model = RoomMember
        fields = (
            'user',
            'room',
            'date_joined'
        )
        depth = 1



class RoomQuizSerializer(serializers.ModelSerializer):
    sponsor = UserSerializer(read_only=True).data
    quiz = QuizSerializer(read_only=True).data
    class Meta:
        model = RoomQuiz
        fields = (
            'sponsor',
            'quiz',
            'date'
        )
        depth = 2



class RoomQuestionSerializer(serializers.ModelSerializer):
    sponsor = UserSerializer(read_only=True).data
    question = QSerializer(read_only=True).data
    class Meta:
        model = RoomQuestion
        fields = (
            'sponsor',
            'question',
            'date'
        )
        depth = 1
        
        
        
class RoomTrueOrFalseQuestionSerializer(serializers.ModelSerializer):
    sponsor = UserSerializer(read_only=True).data
    trueOrFalseQuestion = TrueOrFalseQuestionSerializer(read_only=True).data
    class Meta:
        model = RoomTrueOrFalseQuestion
        fields = (
            'sponsor',
            'trueOrFalseQuestion',
            'date'
        )
        depth = 1
        
        
        
class RoomFourChoicesQuestionSerializer(serializers.ModelSerializer):
    sponsor = UserSerializer(read_only=True).data
    fourChoicesQuestion = FourChoicesQuestionSerializer(read_only=True).data
    class Meta:
        model = RoomFourChoicesQuestion
        fields = (
            'sponsor',
            'fourChoicesQuestion',
            'date'
        )
        depth = 1