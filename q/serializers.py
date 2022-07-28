from rest_framework import serializers
from .models import Q, A, Reply



class QSerializer(serializers.ModelSerializer):
    class Meta:
        model = Q
        fields = ('question', 'description', 'date', 'slug', 'profile')