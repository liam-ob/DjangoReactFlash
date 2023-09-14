from django.urls import path, include
from . import views


app_name = 'core'
urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/register/', views.RegisterUserAPIView.as_view(), name='user-register'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/logout/', views.LogoutView.as_view(), name='logout'),
    path('users/checklogin/', views.CheckLogin.as_view(), name='check-login'),
]
