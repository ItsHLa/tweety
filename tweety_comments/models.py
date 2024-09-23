from django.db import models
from django.shortcuts import get_object_or_404

from accounts.models import Profile
from tweety_posts.models import Post


# Create your models here.


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
    