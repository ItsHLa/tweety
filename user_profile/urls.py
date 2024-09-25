from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    ## info |  delete |  update
    path('',views.ProfileView.as_view(),name='profile'),
    ## follow | unfollow
    path('follow/<pk>', views.FollowView.as_view() , name='follow'),
    # followers
    path('followers/', views.FollowersView.as_view() , name='follower'),
    #following
    path('following/', views.FollowingView.as_view() , name='following'),
]