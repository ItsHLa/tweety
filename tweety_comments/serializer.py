   

from user_profile.serializer import ProfileSerializer
from .models import CommentManager
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content' , "image")
    
    def create(self,validated_data):
        return CommentManager.create_comment(data = validated_data) 
    
    def update(self ,instance,validated_data , **kwargs):
        return CommentManager.update_comment(data = validated_data, comment=instance)
    
class CommentInfoSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    total_like = serializers.SerializerMethodField(method_name="get_total_likes")
    # total_comment = serializers.SerializerMethodField(method_name="get_total_comments") 
    class Meta:
        model = Comment
        fields = ( "id", 'content', "image", "date", "time", "author", "total_like" )
    
    
    def get_total_likes(self , instance):
        return instance.like.count()
    
    