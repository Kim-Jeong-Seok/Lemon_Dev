from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

#from .views import LemonUserAPI
app_name='accounts'

urlpatterns = [
    #path('lemon/', LemonUserAPI),
    path('main', views.main, name='main'),
    path('home', views.home, name='home'),
    path('calendar', views.calendar, name='calendar'),
    path('search_stock', views.search_stock, name='search_stock'),
    path('stock', views.stock, name='stock'),
    path('addlist', views.addlist, name='addlist'),
    path('myinfo', views.myinfo, name='myinfo'),
    path('', views.main, name='main'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_calendar', views.add_calendar, name='add_calendar'),
    
    path('ajax_pushdate/', views.ajax_pushdate, name='ajax_pushdate'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event', views.add_event, name='add_event'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)