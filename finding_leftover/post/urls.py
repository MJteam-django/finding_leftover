from django.contrib import admin
from django.urls import path, include, re_path
from post import views

urlpatterns = [
    path('list/', views.PostListAPIView.as_view(), name="post-list"),
    path('list/<int:pk>', views.PostDetailAPIView.as_view(), name="post-detail"),
    # re_path('^list/search/(?P<username>.+)/$', views.SearchList.as_view()), 
    path("storelist/", views.StoreListAPI.as_view(), name='store-list'),
    path('store/<int:pk>', views.StoreDetailAPIView.as_view(), name="store-detail"),
 
]
