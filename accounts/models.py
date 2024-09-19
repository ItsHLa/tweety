from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.
    # # follow users
    # def follow(self ,profile):
    #     return Follow.objects.create(follow = self ,
    #                           follwers = profile)
    # #unfollow user
    # def unfollow(self , profile):
    #      Follow.objects.filter(follow = self ,
    #                           follwers = profile).delete()
    # # profile that user following
    # def following(self):
    #     return Profile.objects.filter(follows_set_follows = self)
    
    # def followers(self):
    #     return Profile.objects.filter(followers = self)
    
    # def follow_count(self):
    #     return Profile.objects.filter(follows = self).count()
    
    # def follower_count(self):
    #     return Profile.objects.filter(followers = self).count()

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/',blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    
    def update_profile(self , data):
        self.profile_pic = data.get('profile_pic' ,self.profile_pic )
        self.bio = data.get('bio' ,self.bio )
        self.save()
        return self
    
    def delete_profile(self):
        self.delete()
    
    def follow(self, profile):
        return Follow.objects.create(follower = self , follow = profile)
    
    def unfollow(self , profile):
        return Follow.objects.filter(follow = profile , follower = self).delete
    
    def following(self):
        return Follow.objects.filter(follower = self)
    
    def followers(self):
        return Follow.objects.filter(follow = self)
    
    def following_count(self):
        return Follow.objects.filter(follower = self).count
    
    def followers_count(self):
        return Follow.objects.filter(follow = self).count

class Follow (models.Model):
    follow = models.ForeignKey(Profile, related_name='follow', on_delete=models.CASCADE)
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'follow')  # Ensures no duplicate follows

@receiver(post_save , sender = User )
def create_profile(sender , instance , created , **kwargs):
    if created:
        profile = Profile.objects.create(user = instance)
        ## making users follow themselves
        Follow.objects.create(follow = profile , follower = profile)
        