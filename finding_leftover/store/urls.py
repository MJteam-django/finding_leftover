from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    path("", views.StoreListAPI.as_view(), name='store-list'),
    path('<int:pk>', views.StoreDetailAPIView.as_view(), name="store-detail"),
]

