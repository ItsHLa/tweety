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
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/',blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    follows = models.ManyToManyField("self", related_name='followed_by',symmetrical=False)
    
    def update_profile(self , data):
        self.profile_pic = data.get('profile_pic' ,self.profile_pic )
        self.bio = data.get('bio' ,self.bio )
        self.save()
        return self
    
    def delete_profile(self):
        self.delete()
    
    def follow(self, profile):
        return self.follows.add(profile)
    
    def unfollow(self , profile):
        return self.follows.remove(profile)
    
    def following(self):
        return self.follows.all()
    
    def follower(self):
        return self.followed_by.all()
    
    def following_count(self):
        return self.follows.all().count()
    
    def followers_count(self):
        return self.followed_by.all().count()
 
@receiver(post_save , sender = User )
def create_profile(sender , instance , created , **kwargs):
    if created:
        profile = Profile.objects.create(user = instance)
        ## making users follow themselves
        profile.follow(profile=profile)
        