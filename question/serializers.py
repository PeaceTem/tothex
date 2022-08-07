from rest_framework import serializers
from .models import FourChoicesQuestion, TrueOrFalseQuestion
from category.serializers import CategorySerializer

class FourChoicesQuestionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = FourChoicesQuestion
        fields = ('user', 'form', 'question', 'date_created',
        'date_updated', 'answer1', 'answer2', 'answer3', 'answer4',
        'duration_in_seconds', 'categories', 'attempts', 'avgScore',
        'age_from', 'age_to'
        )




class TrueOrFalseQuestionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = TrueOrFalseQuestion
        fields = ('user', 'form', 'question', 'date_created',
        'date_updated', 'answer1', 'answer2',
        'duration_in_seconds', 'categories', 'attempts', 'avgScore',
        'age_from', 'age_to'
        )