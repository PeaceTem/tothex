from django import serialzers
from .models import Quiz

class QuizSerializer(serialzers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('user', 'title', 'description', 'date', 'date_updated', 'when', 'questionLength',
        'totalScore', 'attempts', 'average_score', 'categories', 'duration', 'likes', 'age_from',
        'age_to')