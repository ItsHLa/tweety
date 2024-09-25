from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweety/auth/' , include('accounts.urls')),
    path('tweety/posts/' , include('tweety_posts.urls')),
    path('tweety/comments/' , include('tweety_comments.urls')),
    path('tweety/profile/' , include('user_profile.urls')),
]
