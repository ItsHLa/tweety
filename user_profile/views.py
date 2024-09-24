from .serializer import ProfileInfoSerializer, ProfileSerializer
from .models import Profile
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
        user = request.user
        user.profile.delete_profile()
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
        user.profile.unfollow(profile = profile)
        return Response({'msg':f'You unfollowed @{profile.user.username}'},status= Status.OK)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        if not Profile.objects.filter(pk = pk).exists:
            return Response({'This profile dose not exists'},status= Status.NOT_FOUND)
        profile = Profile.objects.get(pk = pk)
        user.profile.unfollow(profile = profile)
        return Response({'msg':f'You unfollowed @{profile.user.username}'},status= Status.OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    user = request.user
    followers = user.profile.follower()
    serializer = ProfileSerializer(followers , many = True)
    return Response(serializer.data , status=Status.OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    user = request.user
    follows = user.profile.following()
    serializer = ProfileSerializer(follows , many = True)
    return Response(serializer.data , status=Status.OK)