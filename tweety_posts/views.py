
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from tweety_posts.filters import PostFilter
from user_profile.serializer import ProfileInfoSerializer, ProfileSerializer
from user_profile.models import ProfileManager
from utils.status import Status
from .models import  Post, PostManager
from rest_framework.views import APIView
from .serializers import  PostInfoSerializer, PostSerializer

# Create your views here.

## create posts get all_posts
class PostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    ## all posts from followers
    def get(self,request):
        followers = ProfileManager.following(request.user.profile)
        posts = PostManager.news_feeds(followers)
        serializer = PostInfoSerializer(posts , many = True)
        return Response(serializer.data , status=Status.OK)
    
    ## create post
    def post(self,request):
        data = request.data
        user = request.user
        serializer = PostSerializer(data = data)
        if serializer.is_valid():
            serializer.save(author = user.profile)
            return Response(status=Status.OK)
        return Response(serializer.errors , status=Status.BAD_REQUEST)

## update | delete 
class PostDetailsView(APIView):
    permission_classes =[IsAuthenticated]
    
    ## get post detail
    def get(self , request , pk):
        post = PostManager.get_post(pk=pk)
        serializer = PostInfoSerializer(instance=post)
        return Response(serializer.data , status=Status.OK)
    
    ## update post
    def put(self,request,pk):
        data = request.data
        profile = request.user.profile
        post = PostManager.get_post(pk = pk)
        serializer = PostSerializer(instance=post , data=data , partial = True)
        if serializer.is_valid():
            serializer.save(author = profile)
            return Response(serializer.data , status=Status.OK)
        return Response(serializer.errors , status=Status.BAD_REQUEST)
    
    ## delete post
    def delete(self,request,pk):
        PostManager.delete_post(pk)
        return Response({'status':'success'} , status=Status.OK)

# like | unlike
class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    # like post
    def post(self,request,pk):
        user = request.user
        PostManager.add_like(profile=user.profile , pk=pk)
        return Response(status=Status.OK)
    
    # unlike post
    def delete(self,request,pk):
        user = request.user
        PostManager.remove_like(profile=user.profile , pk=pk)
        return Response(status=Status.OK)
    
    # all users who liked post
    def get(self, request,pk, *args, **kwargs):
        who_liked = PostManager.who_liked(pk)
        serializer = ProfileInfoSerializer(who_liked , many = True)
        return Response(serializer.data,status=Status.OK)

# search
class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        filters = PostFilter(request.GET,queryset=Post.objects.all())
        serializer = PostInfoSerializer(data= filters.qs, many= True)
        return Response(serializer.data , status=Status.OK)

