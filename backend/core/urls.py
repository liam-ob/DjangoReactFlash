from django.urls import path, include
from . import views


# /user/
urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('users/login/', views.UserLogin.as_view(), name='user-login'),
]
