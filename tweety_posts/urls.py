from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.PostsView.as_view(),name='posts'),
    path('posts_details/<pk>/',views.PostDetails.as_view(),name='datail_posts'),
    path('likes/<pk>' , views.LikePost.as_view(),name='like_posts')
]
