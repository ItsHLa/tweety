from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from accounts.models import Profile

# Create your models here.

class PostManager():
    @classmethod
    def create_post(self ,data):
        return Post.objects.create(**data)
    
    @classmethod
    def delete_post(self,pk):
        return get_object_or_404(Post , pk = pk).delete()
    
    @classmethod
    def get_post(self,pk):
        return get_object_or_404(Post , pk = pk)
    
    @classmethod
    def update(self,instance,data):
        instance.content = data.get('content' , instance.content)
        instance.image = data.get('image' , instance.image)
        instance.save()
        return instance
    
    @classmethod
    def get_posts(self,instance):
        return instance.post.all()

class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='post', on_delete=models.CASCADE)
    content = models.TextField(max_length=500 , null= True)
    image = models.ImageField(upload_to='posts/images' , null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    objects = PostManager()
    
    


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    author = models.ForeignKey( Profile, related_name='comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='posts/images')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    