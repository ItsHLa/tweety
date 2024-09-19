from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('add_post/', views.add_post , name='add_post'),
    path('update_post/<pk>/', views.update_post , name='update_post'),
    path('delete_post/<pk>/', views.delete_post , name='delete_post'),
]