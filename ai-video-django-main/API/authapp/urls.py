from django.urls import path
# from .views import RegisterView, LoginView, UserView, LogoutView, Prompt, Sotries, Home

from django.contrib import admin
from . import views
from authapp.views import *
urlpatterns = [
    path('',mode1,name="home"),
    path('home',mode1,name="home"),
    path('about/',mode2,name="about"),
    path('signup/',views.SignupPage.as_view(),name='signup'),
    path('login/',views.LoginPage.as_view(),name='login'),
    path('logout/',views.LogoutPage.as_view(),name='logout'),
    path('prompt' , views.Prompt.as_view(), name='prompt'),
    path('success', views.Success.as_view() , name='success'),
    path('stories' , views.Userstories.as_view(), name='stories')
    
]