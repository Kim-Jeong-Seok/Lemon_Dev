"""lemon URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

from rest_framework import routers
#from accounts.views import LemonViewSet
from django.views.generic import TemplateView

#router = routers.DefaultRouter()
#router.register('accounts',LemonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('',include('calendars.urls')),
    path('',include('admins.urls')),
    path('',include('stocks.urls')),
    path('social/', include('allauth.urls')),
#    path(r'^', include(router.urls)),
    path('.*', TemplateView.as_view(template_name='index.html')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
