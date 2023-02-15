from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginuser/', views.login_page, name='loginuser'),
    path('registeruser/', views.registration, name='registeruser'),
    path('main/', views.main_page, name='main_page'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('profile/', views.profile, name='profile'),
    path('request_profile/<str:user_id>', views.requested_user, name='request_profile')
]
