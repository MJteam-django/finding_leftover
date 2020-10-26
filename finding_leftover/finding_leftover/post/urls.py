from django.contrib import admin
from django.urls import path, include, re_path
from post import views

urlpatterns = [
    path('list/', views.PostListAPIView.as_view(), name="post-list"),
    path('list/<int:pk>', views.PostDetailAPIView.as_view(), name="post-detail"),
    # re_path('^list/search/(?P<username>.+)/$', views.SearchList.as_view()), 
    # path("storelist/", views.StoreListAPI.as_view()), #모든 식당의 리스트
    # path("storelist/<str:storename>/", views.SearchStoreList.as_view()), #원하는 식당이름으로 검색

]
