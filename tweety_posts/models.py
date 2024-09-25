from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from user_profile.models import Profile


# Create your models here.

class PostManager(models.Manager):
    
    def create_post(data):
        return Post.objects.create(**data)
    
    def delete_post(pk):
        return get_object_or_404(Post , pk = pk).delete()
    
    def get_post(pk):
        return get_object_or_404(Post , pk = pk)
    
    def update_post(post, data):
        post.content = data.get('content' , post.content)
        post.image = data.get('image' , post.image)
        post.save()
        return post
    
    def who_liked(pk):
        return get_object_or_404(Post , pk = pk).like.all()
    
    
    def add_like(pk, profile):
        return get_object_or_404(Post , pk = pk).like.add(profile)
    
    def remove_like(pk, profile):
        return get_object_or_404(Post,pk=pk).like.remove(profile)
        
    def news_feeds(profiles):
        return Post.objects.all().filter(author__in =profiles)
    
    ## put in profile

    # def get_posts_by_author(cls,author):
    #     return author.post.all()

class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='post', on_delete=models.CASCADE)
    content = models.TextField(max_length=500 , null= True)
    image = models.ImageField(upload_to='posts/images' , null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    like = models.ManyToManyField(Profile , related_name="post_liked_by")
    
    objects = PostManager()