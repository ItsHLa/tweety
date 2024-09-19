from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

# Register your models here.
class InlineProfile(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    
    fields = ['username' , 'email','password']
    inlines = [InlineProfile]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
