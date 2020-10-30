from django.contrib import admin
from django.urls import path, include, re_path
from post import views

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name="post-list"),
    path('<int:pk>', views.PostDetailAPIView.as_view(), name="post-detail"),
    
    path('create/', views.PostCreateAPIView.as_view(), name="post-create"), 
    path('update/<int:pk>', views.PostUpdateAPIView.as_view(), name="post-update"),

]
