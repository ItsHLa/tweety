from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from accounts.models import Profile

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
        return instance.update_profile(data = validated_data)


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password')
    
    def create(self , validated_data):
        return User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = make_password(validated_data['password']),
        )
        
class LoginSerializer(ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields =("email" , "password")
    
    def check_user(self ,validate_data):
        email = validate_data["email"]
        if not User.objects.filter(email = email):
            return None
        user = User.objects.get(email = email)
        return user