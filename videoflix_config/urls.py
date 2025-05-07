"""
URL configuration for videoflix_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings  
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render

schema_view = get_schema_view(
   openapi.Info(
      title="Videoflix API",
      default_version='v1',
      description="API Dokumentation für Videoflix",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

def api_home(request):
    return render(request, 'api_home.html')

urlpatterns = [
    path('', api_home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.api.urls')),
    path('api/movie/', include('movie_app.api.urls')),
    path('__debug__', include('debug_toolbar.urls')),
    path('django-rq/', include('django_rq.urls')),

    # Swagger und Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + staticfiles_urlpatterns()  

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def custom_404(request, exception):
    return render(request, "404.html", status=404)

handler404 = 'videoflix_config.urls.custom_404'
