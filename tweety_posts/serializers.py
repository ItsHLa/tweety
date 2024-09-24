from rest_framework import serializers

from user_profile.serializer import ProfileSerializer


from .models import  Post, PostManager

class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only = True)
    total_like = serializers.SerializerMethodField()
    total_comment = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ( "id",'content' , "image" , "date" , "time" ,"author","total_like","total_comment")
    
    def create(self,validated_data):
        return PostManager.create_post(data = validated_data) 
    
    def update(self ,instance,validated_data , **kwargs):
        return PostManager.update(data = validated_data, instance=instance)
    
    def get_total_likes(self , instance):
        return instance.like.count()
    
    def get_total_comments(self , instance):
        return instance.author_comment.count()
 