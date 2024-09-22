from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from accounts.models import Profile

# Create your models here.

class PostManager(models.Manager):
    @classmethod
    def create_post(cls ,data):
        return Post.objects.create(**data)
    
    @classmethod
    def delete_post(cls,pk):
        return get_object_or_404(Post , pk = pk).delete()
    
    @classmethod
    def get_post(cls,pk):
        return get_object_or_404(Post , pk = pk)
    
    @classmethod
    def update(cls,instance,data):
        instance.content = data.get('content' , instance.content)
        instance.image = data.get('image' , instance.image)
        instance.save()
        return instance
    
    @classmethod
    def who_liked(cls , pk):
        return get_object_or_404(Post , pk = pk).liked_by.all()
    
    @classmethod
    def total_likes(cls , pk):
        return get_object_or_404(Post , pk = pk).liked_by.all().count()
    
    @classmethod
    def add_like(cls,pk,user):
        return get_object_or_404(Post , pk = pk).like.add(user)
    
    @classmethod
    def remove_like(cls,pk,user):
        return get_object_or_404(Post,pk=pk).liked_by.remove(user)
    
    @classmethod
    def get_comments(cls,pk):
        get_object_or_404(Post,pk=pk).author_comment.all()
        
    @classmethod
    def total_comments(cls,pk):
        get_object_or_404(Post,pk=pk).author_comment.all().count()
    
    ## put in profile
    @classmethod
    def get_posts_by_author(cls,author):
        return author.post.all()

class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='post', on_delete=models.CASCADE)
    content = models.TextField(max_length=500 , null= True)
    image = models.ImageField(upload_to='posts/images' , null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    like = models.ManyToManyField(Profile , related_name="post_liked_by")
    
    objects = PostManager()
    
    

class CommentManager(models.Manager):
    @classmethod
    def create_comment(cls ,data):
        return Comment.objects.create(**data)
    
    @classmethod
    def delete_post(cls,pk):
        return get_object_or_404(Comment , pk = pk).delete()
    
    @classmethod
    def update(cls,comment,data):
        comment.content = data.get('content' , comment.content)
        comment.image = data.get('image' , comment.image)
        comment.save()
        return comment
    
    @classmethod
    def who_liked(cls , pk):
        return get_object_or_404(Comment , pk = pk).liked_by.all()
    
    @classmethod
    def total_likes(cls , pk):
        return get_object_or_404(Comment , pk = pk).liked_by.all().count()
    
    @classmethod
    def add_like(cls,pk,user):
        return get_object_or_404(Comment , pk = pk).like.add(user)
    
    @classmethod
    def remove_like(cls,pk,user):
        return get_object_or_404(Comment,pk=pk).liked_by.remove(user)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    author = models.ForeignKey( Profile, related_name='author_comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='posts/images' , null=True , blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    like = models.ManyToManyField(Profile , related_name="comment_liked_by")
    