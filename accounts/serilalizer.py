from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer (ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' ]


class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password')
    
    def create(self , validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class LoginSerializer(ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields =("email" , "password")