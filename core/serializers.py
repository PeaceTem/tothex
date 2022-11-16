from rest_framework import serializers
# from category.models import Category
from .models import *
from category.serializers import CategorySerializer

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name'
            )



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True).data
    categories = CategorySerializer(many=True, read_only=True).data
    class Meta:
        model = Profile
        fields = (
            'user',
            'picture',
            'bio',
            'gender',
            'date_of_birth',
            'state_of_residence',
            'state_of_origin',
            'nationality',
            'coins',
            'total_coins',
            'quizAvgScore',
            'questionAvgScore',
            'categories',
            'views',
            'refercount'
            )
        depth = 2


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True).data
    followers = UserSerializer(many=True, read_only=True).data
    following = UserSerializer(many=True, read_only=True).data

    class Meta:
        model = Follower
        fields = (
            'user',
            'followers',
            'following'
            )
        depth = 1




class StreakSerializer(serializers.Serializer):
    profile = ProfileSerializer(read_only=True).data
    class Meta:
        model = Streak
        fields = (
            'profile',
            'active',
            'length',
            'question',
            'freeze'
            )
        depth = 2



class LinkSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True).data

    class Meta:
        model = Link
        fields = (
            'profile',
            'name',
            'link',
            'description',
            'clicks'
            )
        depth = 2



        
class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = (
            'title',
            'feedback'
            )


        