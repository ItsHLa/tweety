from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


from django.contrib.auth.models import User
from accounts.serilalizer import  LoginSerializer, SignUpSerializer
from accounts.utils import Tokens
from utils.status import Status
# Create your views here.


class SignUpView(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter().exists():
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


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def follow(request , pk):
#     user = request.user
#     if not Profile.objects.filter(pk = pk).exists:
#         return Response({'This profile dose not exists'},status=status.HTTP_404_NOT_FOUND)
#     profile = Profile.objects.get(pk = pk)
#     user.profile.follow(profile)
#     return Response({'msg':f'You follow @{profile.user.username} now!'},status=status.HTTP_200_OK)
    
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def unfollow(request , pk ):
#     user = request.user
#     if not Profile.objects.filter(pk = pk).exists:
#         return Response({'This profile dose not exists'},status=status.HTTP_404_NOT_FOUND)
#     profile = Profile.objects.get(pk = pk)
#     user.profile.unfollow(profile = profile)
#     return Response({'msg':f'You unfollowed @{profile.user.username}'},status=status.HTTP_200_OK)
    
    


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def profile_info(request):
#     user = request.user
#     follow_count = user.profile.following_count()
#     follower_count = user.profile.followers_count()
#     serializer = ProfileSerializer(instance=user.profile)
#     return Response({
#         'info':serializer.data,
#         'followers_count':follower_count,
#         'follows_count':follow_count} , status=status.HTTP_200_OK)

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def profile_update(request):
#     user = request.user
#     data = request.data
#     serializer = ProfileSerializer(instance=user.profile , data=data , partial = True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data , status=status.HTTP_200_OK)
#     return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def profile_delete(request):
#     user = request.user
#     data = request.data
#     user.profile.delete_profile()
#     return Response( status=status.HTTP_200_OK)




