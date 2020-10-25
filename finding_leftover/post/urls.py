from django.contrib import admin
from django.urls import path, include, re_path
from post import views

urlpatterns = [
    path('list/', views.PostList.as_view(), name="post-list"),
    path('list/<int:pk>', views.PostRetrieveDestroy.as_view(), name="post-detail"),
    re_path('^list/search/(?P<username>.+)/$', views.SearchList.as_view()),
]
