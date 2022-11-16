from rest_framework import serializers

from core.serializers import ProfileSerializer
from .models import Q, A, Reply



class QSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True).data

    class Meta:
        model = Q
        fields = (
            'question',
            'question_image',
            'description',
            'date',
            'date_updated',
            'profile'
            )
        depth = 2



class ASerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True).data
    class Meta:
        model = A
        fields = (
            'profile',
            'answer',
            'solution_image'
            )
        depth = 2



class ReplySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True).data
    answer = ASerializer(read_only=True).data

    class Meta:
        model = Reply
        fields = (
            'answer',
            'profile',
            'reply',
            'date',
            'date_updated'
            )
        depth = 2



