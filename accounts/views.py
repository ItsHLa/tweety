from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from accounts.serilalizer import  ChangePasswordSerializer, LoginSerializer, LogoutSerializer, SignUpSerializer, UserSerializer
from accounts.utils import Tokens
from utils.status import Status
# Create your views here.


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SignUpSerializer(data=data , partial = True)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            if User.objects.filter(email =email).exists():
                Response({"msg":"User already exists "} , status=Status.BAD_REQUEST)
            
            user = serializer.save()
            token = Tokens.genarate_tokens(user)
            return Response({
                "msg" : f" Welcom {user.username} ",
                'refresh':token["refresh"],
                "access":token["access"]
                },status=Status.CREATED)
                
        return Response(serializer.errors , status=Status.BAD_REQUEST)            
            
class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data = data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            if not User.objects.filter(email = email).exists():
                return Response({'msg':'User Not Found'},status=Status.NOT_FOUND)
            user = User.objects.get(email = email)
            if not user.check_password(password):
                return Response({'msg':'Password dose not match'},status=Status.BAD_REQUEST)
            token = Tokens.genarate_tokens(user)
            return Response({
                "msg":f'Welcom Back {user.username}',
                "refresh":token['refresh'],
                "access":token['access']
            },status=Status.OK)
        return Response(serializer.errors , status=Status.BAD_REQUEST)

class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = UserSerializer(instance=user, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=Status.OK)
        return Response(serializer.errors ,status=Status.BAD_REQUEST)

class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = LogoutSerializer(data=data)
        if serializer.is_valid():
            Tokens.blacklist_token(serializer.validated_data['refresh'])
            return Response({"msg":"Sad to see you go :("},status=Status.OK)
        return Response(serializer.errors ,status=Status.BAD_REQUEST)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = ChangePasswordSerializer(instance=user, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=Status.OK)
        return Response(serializer.errors ,status=Status.BAD_REQUEST)