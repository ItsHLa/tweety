from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.serilalizer import  LoginSerializer, ProfileSerializer, SignUpSerializer, UserSerializer
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request , pk):
    user = request.user
    if not Profile.objects.filter(pk = pk).exists:
        return Response({'This profile dose not exists'},status=status.HTTP_404_NOT_FOUND)
    profile = Profile.objects.get(pk = pk)
    user.profile.follow(profile)
    return Response({'msg':f'You follow @{profile.user.username} now!'},status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow(request , pk ):
    user = request.user
    if not Profile.objects.filter(pk = pk).exists:
        return Response({'This profile dose not exists'},status=status.HTTP_404_NOT_FOUND)
    profile = Profile.objects.get(pk = pk)
    user.profile.unfollow(profile = profile)
    return Response({'msg':f'You unfollowed @{profile.user.username}'},status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    user = request.user
    followers = user.profile.follower()
    serializer = ProfileSerializer(followers , many = True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    user = request.user
    follows = user.profile.following()
    serializer = ProfileSerializer(follows , many = True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_info(request):
    user = request.user
    follow_count = user.profile.following_count()
    follower_count = user.profile.followers_count()
    serializer = ProfileSerializer(instance=user.profile)
    return Response({
        'info':serializer.data,
        'followers_count':follower_count,
        'follows_count':follow_count} , status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    user = request.user
    data = request.data
    serializer = ProfileSerializer(instance=user.profile , data=data , partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request):
    user = request.user
    data = request.data
    user.profile.delete_profile()
    return Response( status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    data = request.data
    
    if User.objects.filter(username = data['username'] , email = data['email']).exists():
        return Response({'msg': "user already logged in"})
    
    serializer = SignUpSerializer(data = data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user=user)
        return Response({'msg': "user signed up",
             "access":str(refresh.access_token),
             "refresh":str(refresh)
             } , status= status.HTTP_201_CREATED)
    return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        user = serializer.check_user()
        if user is None:
            return Response({"msg":"user dose not exists"} , status= status.HTTP_400_BAD_REQUEST)
        if not check_password(user.password ,data['pass'] ):
            pass
            