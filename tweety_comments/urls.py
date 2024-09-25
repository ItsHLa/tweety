from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
   path('<pk>/',views.CommentView.as_view(),name="comment"),
   path('like/<pk>/',views.LikeView.as_view(),name="like"),
]