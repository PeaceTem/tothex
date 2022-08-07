from rest_framework import serializers
from .models import Quiz
from category.serializers import CategorySerializer
class QuizSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True).data
    class Meta:
        model = Quiz
        fields = ('user', 'title', 'description', 'date', 'date_updated', 'when', 'questionLength',
        'totalScore', 'attempts', 'average_score', 'categories', 'duration', 'likes', 'age_from',
        'age_to')
        depth=1