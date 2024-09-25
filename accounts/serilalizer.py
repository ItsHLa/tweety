from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import UserManager

class UserSerializer (ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username" , "email", "first_name", "last_name" , "password")
    
    def create(self , validated_data):
        return UserManager.create_user(validated_data)
    
    def update(self , instance, validated_data):
        return UserManager.update_user(user=instance, data=validated_data)

class ChangePasswordSerializer (ModelSerializer):
    old_password = serializers.CharField(max_length = 6)
    new_password = serializers.CharField(max_length = 6)
    class Meta:
        model = User
        fields = ("old_password" ,"new_password" )
    
    def update(self , instance, validated_data):
         return UserManager.change_password(user=instance, data=validated_data)



class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password')
    
    
class LoginSerializer(ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields =("email" , "password")

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()