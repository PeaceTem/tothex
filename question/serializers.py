from django import serialzers
from .models import FourChoicesQuestion, TrueOrFalseQuestion


class FourChoicesQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FourChoicesQuestion
        fields = ('user', 'form', 'question', 'date_created',
        'date_updated', 'answer1', 'answer2', 'answer3', 'answer4',
        'duration_in_seconds', 'categories', 'attempts', 'avgScore',
        'age_from', 'age_to'
        )




class TrueOrFalseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FourChoicesQuestion
        fields = ('user', 'form', 'question', 'date_created',
        'date_updated', 'answer1', 'answer2',
        'duration_in_seconds', 'categories', 'attempts', 'avgScore',
        'age_from', 'age_to'
        )