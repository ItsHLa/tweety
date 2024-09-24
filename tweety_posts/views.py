
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from tweety_posts.filters import PostFilter
from user_profile.serializer import ProfileSerializer
from user_profile.models import ProfileManager
from .models import  Post, PostManager
from rest_framework.views import APIView
from .serializers import  PostSerializer

# Create your views here.

## create posts get all_posts
class PostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    ## all posts from followers
    def get(self,request):
        followers = ProfileManager.following(request.user.profile)
        posts = PostManager.news_feeds(followers)
        serializer = PostSerializer(posts , many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    ## create post
    def post(self,request):
        data = request.data
        user = request.user
        serializer = PostSerializer(data = data)
        if serializer.is_valid():
            serializer.save(author = user.profile)
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

## update | delete 
class PostDetailsView(APIView):
    permission_classes =[IsAuthenticated]
    
    ## get post detail
    def get(self , request , pk):
        post = PostManager.get_post(pk=pk)
        serializer = PostSerializer(instance=post)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    ## update post
    def put(self,request,pk):
        data = request.data
        profile = request.user.profile
        post = PostManager.get_post(pk = pk)
        serializer = PostSerializer(instance=post , data=data , partial = True)
        if serializer.is_valid():
            serializer.save(author = profile)
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    ## delete post
    def delete(self,request,pk):
        PostManager.delete_post(pk)
        return Response({'status':'success'} , status=status.HTTP_200_OK)

# like | unlike
class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    # like post
    def post(self,request,pk):
        user = request.user
        PostManager.add_like(user=user , pk=pk)
        return Response(status=status.HTTP_200_OK)
    
    # unlike post
    def delete(self,request,pk):
        user = request.user
        PostManager.remove_like(user=user , pk=pk)
        return Response(status=status.HTTP_200_OK)
    
    # all users who liked post
    def get(self, request,pk, *args, **kwargs):
        who_liked = PostManager.who_liked(pk)
        serializer = ProfileSerializer(who_liked)
        return Response(serializer,status=status.HTTP_200_OK)

# search
class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        filters = PostFilter(request.GET,queryset=Post.objects.all())
        serializer = PostSerializer(data= filters.qs, many= True)
        return Response(serializer.data , status=status.HTTP_200_OK)

