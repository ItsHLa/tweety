from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.PostsView.as_view(),name='posts'),
    path('posts_details/<pk>/',views.PostDetailsView.as_view(),name='datail_posts'),
    path('likes/<pk>' , views.LikeView.as_view(),name='like_posts'),
    path('search/' , views.SearchView.as_view(),name='like_posts')
]
