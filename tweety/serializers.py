from rest_framework import serializers

from accounts.serilalizer import ProfileSerializer
from tweety.models import Post, PostManager

class PostSerallizer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only = True)
    class Meta:
        model = Post
        fields = ( "id",'content' , "image" , "date" , "time" ,"author" )
    
    def create(self,validated_data):
        return PostManager.create_post(data = validated_data) 
    
    def update(self ,instance,validated_data , **kwargs):
        return PostManager.update(data = validated_data, instance=instance)