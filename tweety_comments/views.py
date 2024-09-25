from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tweety_comments.models import CommentManager
from tweety_comments.serializer import CommentInfoSerializer, CommentSerializer
from rest_framework.views import APIView

from tweety_posts.models import PostManager
from user_profile.serializer import ProfileInfoSerializer
from utils.status import Status

    

class CommentView(APIView):
    permission_classes =[IsAuthenticated]
    # create comment
    def post(self,request,pk):
        data = request.data
        user = request.user
        post = PostManager.get_post(pk=pk)
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save(post = post,author = user.profile)
            return Response(status=Status.OK)
        return Response(serializer.errors , status=Status.BAD_REQUEST)
    
    #get all comments
    def get(self,request,pk):
        post = PostManager.get_post(pk = pk)
        comments = CommentManager.get_comments(post)
        serializer = CommentInfoSerializer(comments ,many=True)
        return Response(serializer.data , status=Status.OK)
    
    ## update comment
    def put(self,request,pk):
        data = request.data
        profile = request.user.profile
        comment = CommentManager.get_comment(pk = pk)
        serializer = CommentSerializer(instance=comment , data=data , partial = True)
        if serializer.is_valid():
            serializer.save(author = profile)
            return Response(serializer.data , status=Status.OK)
        return Response(serializer.errors , status=Status.BAD_REQUEST)
    
    #delete comment
    def delete(self,request,pk):
        CommentManager.delete_comment(pk)
        return Response({'status':'success'} , status=Status.OK)

class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    # like comment
    def post(self,request,pk):
        user = request.user
        CommentManager.add_like(profile=user.profile , pk=pk)
        return Response(Status.OK)
    
    # unlike comment
    def delete(self,request,pk):
        user = request.user
        CommentManager.remove_like(profile=user.profile , pk=pk)
        return Response(status=Status.OK)
    
    # all users who liked comment
    def get(self, request,pk, *args, **kwargs):
        who_liked = CommentManager.who_liked(pk)
        serializer = ProfileInfoSerializer(who_liked , many = True)
        return Response(serializer.data,status=Status.OK)