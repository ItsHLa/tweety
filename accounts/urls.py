from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [
    path('signup/', views.signup , name='signup'),
    path('get_followers/', views.get_followers , name='get_followers'),
]