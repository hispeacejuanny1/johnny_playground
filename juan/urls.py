#juan/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')),  # 홈화면을 games 앱이 담당
    path('community/', include('community.urls')),   
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('games/', include('games.urls')),
]
