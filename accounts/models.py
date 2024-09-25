from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserManager(models.Manager):
    
    def create_user(data):
        user = User.objects.create(
            username = data['username'],
            email = data['email']
        )
        user.set_password(data['password'])
        user.save()
        return user
    
    def update_user(user , data):
        user.first_name = data.get('first_name' , user.first_name)
        user.last_name = data.get('last_name' , user.last_name)
        user.username = data.get('username' , user.username)
        user.email = data.get('email' , user.email)
        user.save()
        return user
    
    def change_password(user,data):
        if user.check_password(data.get('old_password',"")):
            user.set_password(data['new_password'])
            user.save()
        return user
    
    def delete_user(user):
        user.delete()