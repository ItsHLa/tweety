from django.db import models
from django.shortcuts import get_object_or_404


from tweety_posts.models import Post
from user_profile.models import Profile


# Create your models here.


class CommentManager(models.Manager):

    def create_comment(data):
        return Comment.objects.create(**data)
    
    def delete_comment(pk):
        return get_object_or_404(Comment , pk = pk).delete()

    def update_comment(comment, data):
        comment.content = data.get('content' , comment.content)
        comment.image = data.get('image' , comment.image)
        comment.save()
        return comment
    
    def who_liked(pk):
        return get_object_or_404(Comment , pk = pk).like.all()
    
    
    def add_like(pk, profile):
        return get_object_or_404(Comment , pk = pk).like.add(profile)
    
    def remove_like(pk, profile):
        return get_object_or_404(Comment,pk=pk).like.remove(profile)
    
    def get_comments(post):
        return post.post_comment.all()
    
    def get_comment(pk):
        return get_object_or_404(Comment , pk = pk)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    author = models.ForeignKey( Profile, related_name='author_comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='comments/images' , null=True , blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    like = models.ManyToManyField(Profile , related_name="comment_liked_by")
    