from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ProfileManager

class UserSerializer (ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' ]

class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['id','user','profile_pic','bio']
    
    def update(self ,instance, validated_data , **kwargs):
        return ProfileManager.update_profile(data = validated_data , profile=instance)

class ProfileInfoSerializer(ModelSerializer):
    user = UserSerializer()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id','user','profile_pic','bio','followers','following']
    
    def total_followers(self , profile):
        return profile.followed_by.count()
    
    def total_following(self , profile):
        return profile.follows.count()