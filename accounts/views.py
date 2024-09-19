from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from accounts.models import Profile
from accounts.serilalizer import  ProfileSerializer, SignUpSerializer, UserSerializer
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request , profile_pk):
    user = request.user
    profile = Profile.objects.filter(pk = profile_pk)
    if profile:
        follow = user.profile.follow(profile)
        if follow:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow(request , profile_pk ):
    user = request.user
    profile = Profile.objects.filter(pk = profile_pk)
    user.profile.unfollow(profile = profile)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    user = request.user
    followers = user.profile.followers()
    serializer = ProfileSerializer(followers , many = True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    user = request.user
    follows = user.following()
    serializer = UserSerializer(data = follows , many = True)
    return Response(serializer.data , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_info(request):
    user = request.user
    follow_count = user.profile.follow_count()
    follower_count = user.profile.follower_count()
    serializer = ProfileSerializer(data=user.profile)
    info = {
        'info':serializer.data,
        'followers_count':follower_count,
        'follows_count':follow_count} 
    return Response(info , status=status.HTTP_200_OK)

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