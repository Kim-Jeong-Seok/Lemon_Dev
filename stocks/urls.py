from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from stocks import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'stocks'

urlpatterns = [
    path('search_stock', views.search_stock, name='search_stock'),
    path('stock', views.stock, name='stock'),
    path('portfolio', views.portfolio, name='portfolio'),

    path('current_stock', views.current_stock, name='current_stock'),
    path('buy_stock', views.buy_stock, name='buy_stock'),
    path('sold_stock', views.sold_stock, name='sold_stock'),
    path('get_selectivemaster', views.get_selectivemaster, name='get_selectivemaster'),
    path('stocksector_update', views.stocksector_update, name='stocksector_update'),
    path('get_history', views.get_history, name='get_history'),
]
