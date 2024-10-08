"""obm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from .views import get_popular_search_rank
urlpatterns = [
    path('admin/', admin.site.urls),
    path('img/', include('img.urls')),
    path('accounts/', include('accounts.urls')),
    
    path('', views.main, name = 'main'),
    path('get_popular_search_rank/', get_popular_search_rank, name='get_popular_search_rank'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
