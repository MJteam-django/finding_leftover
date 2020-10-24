from django.contrib import admin
from django.urls import path, include
from post import views

urlpatterns = [
    path('list/', views.PostList.as_view()),
    path('list/<int:pk>', views.PostRetrieveDestroy.as_view()),



]
