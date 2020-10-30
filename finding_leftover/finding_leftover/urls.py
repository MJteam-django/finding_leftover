from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('store/', include('store.urls')),
    path('account/', include('account.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
