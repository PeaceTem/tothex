from rest_framework import serializers
from .models import Attempter, Quiz, QuizLink
from category.serializers import CategorySerializer
from core.serializers import UserSerializer
# create a user serializer
# create a serializer for every object of these app



class QuizSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True).data
    categories = CategorySerializer(many=True, read_only=True).data
    class Meta:
        model = Quiz
        fields = ('user', 'title', 'description', 'date', 'date_updated', 'when', 'questionLength',
        'totalScore', 'attempts', 'average_score', 'categories', 'duration', 'likes', 'age_from',
        'age_to')
        depth=1

class QuizLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizLink
        fields = ('name', 'link', 'description', 'clicks')


class AttempterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True).data
    class Meta:
        model = Attempter
        fields = ('user', 'score', 'percentage', 'timeTaken')
        depth = 1
