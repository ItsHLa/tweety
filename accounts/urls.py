from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view() , name='signup'),
    path('login/', views.LoginView.as_view() , name='login'),
    path('logout/', views.LogoutView.as_view() , name='logout'),
    path('userInfo/',views.UpdateUserInfoView.as_view(),name="userInfo"),
    path('changepassword/',views.ChangePasswordView.as_view(),name="changepassword"),
]