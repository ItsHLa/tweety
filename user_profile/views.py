from .serializer import ProfileInfoSerializer, ProfileSerializer
from .models import Profile, ProfileManager
from utils.status import Status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    #get profile info
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileInfoSerializer(instance=profile)
        return Response(serializer.data ,status= Status.OK)
        
        
    # delete 
    def delete(self, request, *args, **kwargs):
        profile = request.user
        ProfileManager.delete_profile(profile)
        return Response(status= Status.OK)
    
    # update
    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = ProfileSerializer(instance=user.profile , data=data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= Status.OK)
        return Response(serializer.errors , status= Status.BAD_REQUEST)

# follow | unfollow
class FollowView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk, *args, **kwargs):
        user = request.user
        if not Profile.objects.filter(pk = pk).exists:
            return Response({'This profile dose not exists'},status= Status.NOT_FOUND)
        profile = Profile.objects.get(pk = pk)
        ProfileManager.unfollow(follow= profile,follower=user.profile)
        return Response({'msg':f'You unfollowed @{profile.user.username}'},status= Status.OK)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        if not Profile.objects.filter(pk = pk).exists:
            return Response({'This profile dose not exists'},status= Status.NOT_FOUND)
        profile = Profile.objects.get(pk = pk)
        ProfileManager.follow(follow= profile,follower=user.profile)
        return Response({'msg':f'You followed @{profile.user.username}'},status= Status.OK)

class FollowersView(APIView):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        followers = ProfileManager.follower(profile)
        serializer = ProfileSerializer(followers , many = True)
        return Response(serializer.data , status=Status.OK)

class FollowingView(APIView):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        followers = ProfileManager.following(profile)
        serializer = ProfileSerializer(followers , many = True)
        return Response(serializer.data , status=Status.OK)
