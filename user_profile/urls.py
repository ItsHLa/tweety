from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [
    ## following stuff
    # path('get_following/', views.get_following , name='get_following'),
    # path('get_followers/', views.get_followers , name='get_followers'),
    # path('follow/<pk>', views.follow , name='followe'),
    # path('unfollow/<pk>', views.unfollow , name='unfollow'),
    # ## profile stuff
    # path('profile_info/', views.profile_info , name='profile_info'),
]