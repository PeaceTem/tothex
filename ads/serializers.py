from rest_framework import serializers
from .models import PostAd

class PostAdSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostAd
        fields = (
            'name',
            'picture',
            'description',
            'link'
            )