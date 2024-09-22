from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tweety.models import Post, PostManager
from rest_framework.views import APIView
from tweety.serializers import PostSerallizer

# Create your views here.


class PostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        data = request.data
        user = request.user
        serializer = PostSerallizer(data = data)
        if serializer.is_valid():
            serializer.save(author = user.profile)
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    

class PostDetails(APIView):
    permission_classes =[IsAuthenticated]
    
    def put(self,request,pk):
        data = request.data
        profile = request.user.profile
        post = PostManager.get_post(pk = pk)
        serializer = PostSerallizer(instance=post , data=data , partial = True)
        if serializer.is_valid():
            serializer.save(author = profile)
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        PostManager.delete_post(pk)
        return Response({'status':'success'} , status=status.HTTP_200_OK)