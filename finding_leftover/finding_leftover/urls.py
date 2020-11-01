from django.contrib import admin
from django.urls import path, include
from finding_leftover.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('post/', include('post.urls')),
    path('store/', include('store.urls')),
    path('account/', include('account.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
