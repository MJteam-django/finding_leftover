from django.contrib import admin
from django.urls import path, include
from store import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
urlpatterns = [
    path("", views.StorenameListAPI.as_view(), name='store-name-list'),
    path("local", views.StorelocalListAPI.as_view(), name='store-local-list'),
    path('<int:pk>', views.StoreDetailAPIView.as_view(), name="store-detail"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

