from rest_framework import serializers

from user_profile.serializer import ProfileSerializer


from .models import  Post, PostManager

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ( 'content' , "image" , "date" , "time" )
    
    def create(self,validated_data):
        return PostManager.create_post(data = validated_data) 
    
    def update(self ,instance,validated_data , **kwargs):
        return PostManager.update_post(data = validated_data, post=instance)
    

class PostInfoSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    total_like = serializers.SerializerMethodField(method_name="get_total_likes")
    total_comment = serializers.SerializerMethodField(method_name="get_total_comments") 
    class Meta:
        model = Post
        fields = ( "id", 'content', "image", "date", "time", "author", "total_like", "total_comment")
    
    
    def get_total_likes(self , instance):
        return instance.like.count()
    
    def get_total_comments(self , instance):
        return instance.post_comment.count()
 