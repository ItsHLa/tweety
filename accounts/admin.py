from django.contrib import admin

from django.contrib.auth.models import User

from user_profile.models import Profile

# Register your models here.
class InlineProfile(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    
    fields = ['username' , 'email','password']
    inlines = [InlineProfile]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
