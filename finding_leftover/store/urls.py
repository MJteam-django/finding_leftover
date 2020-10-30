from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    path("", views.StorenameListAPI.as_view(), name='store-list'),
    path("local", views.StorelocalListAPI.as_view(), name='store-local-list'),
    path('<int:pk>', views.StoreDetailAPIView.as_view(), name="store-detail"),
]

