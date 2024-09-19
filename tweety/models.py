from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from accounts.models import Profile

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='post', on_delete=models.CASCADE)
    content = models.TextField(max_length=500 , null= True)
    image = models.ImageField(upload_to='posts/images' , null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    @staticmethod
    def create_post(data):
        return Post.objects.create(**data)
    
    def update(self ,data):
        self.content = data.get('content' , self.content)
        self.image = data.get('image' , self.image)
        self.save()
        return self
    
    @staticmethod
    def delete_post(pk):
        return get_object_or_404(Post , pk = pk).delete()
    
    @staticmethod
    def get_post(pk):
        return get_object_or_404(Post , pk = pk)
    
    @staticmethod
    def get_posts(self):
        return self.post.all()
    
    
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    author = models.ForeignKey( Profile, related_name='comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='posts/images')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    