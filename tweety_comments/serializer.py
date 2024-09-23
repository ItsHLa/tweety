   
from accounts.serilalizer import ProfileSerializer

from .models import CommentManager
from tweety_posts import serializers
from tweety_posts.models import Post


class CommentSerallizer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only = True)
    class Meta:
        model = Post
        fields = ( "id",'content' , "image" , "date" , "time" ,"author" ,"like")
    
    def create(self,validated_data):
        return CommentManager.create_post(data = validated_data) 
    
    def update(self ,instance,validated_data , **kwargs):
        return CommentManager.update(data = validated_data, instance=instance)