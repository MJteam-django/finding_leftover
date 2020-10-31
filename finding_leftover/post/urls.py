from django.contrib import admin
from django.urls import path, include, re_path
from post import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name="post-list"),
    path('<int:pk>', views.PostDetailAPIView.as_view(), name="post-detail"),
    
    path('create/', views.PostCreateAPIView.as_view(), name="post-create"), 
    path('update/<int:pk>', views.PostUpdateAPIView.as_view(), name="post-update"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
