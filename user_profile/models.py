from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import  receiver

from accounts.models import UserManager
# Create your models here.

class ProfileManager(models.Manager):
    
    def update_profile(profile, data):
        profile.profile_pic = data.get('profile_pic' ,profile.profile_pic )
        profile.bio = data.get('bio' ,profile.bio )
        profile.save()
        return profile
    
    def delete_profile(profile):
        UserManager.delete()
    
    def follow(follower,follow):
        return follower.follows.add(follow)
    
    def unfollow(follower,follow):
        return follower.follows.remove(follow)
    
    def following(profile):
        return profile.follows.all()
    
    def follower(profile):
        return profile.followed_by.all()
    
    # def following_count(profile):
    #     return profile.follows.all().count()
    
    # def followers_count(profile):
    #     return profile.followed_by.all().count()
    

class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/',blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    follows = models.ManyToManyField("self", related_name='followed_by',symmetrical=False)
      
@receiver(post_save , sender = User )
def create_profile(sender , instance , created , **kwargs):
    if created:
        profile = Profile.objects.create(user = instance)
        ## making users follow themselves
        ProfileManager.follow(follow=profile , follower=profile)
        