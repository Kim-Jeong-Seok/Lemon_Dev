from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from calendars import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'calendars'

urlpatterns = [

    path('', views.home, name='home'),
    path('calendar', views.calendar, name='calendar'),
    path('summary', views.summary, name='summary'), # 요약페이 지
    path('recom', views.recom, name='recom'), # 추천페이지
    path('listview', views.listview, name='listview'), # 내역페이지
    path('detail_search', views.detail_search, name='detail_search'),
    path('add_calendar/', views.add_calendar, name='add_calendar'),
    path('edit_calendar/<str:kind>/<int:spend_id>/', views.edit_calendar, name='edit_calendar'),
    path('sedit_calendar/<int:spend_id>', views.sedit_calendar, name='sedit_calendar'),
    path('iedit_calendar/<int:spend_id>', views.iedit_calendar, name='iedit_calendar'),

    path('ajax_pushdate', views.ajax_pushdate, name='ajax_pushdate'),

    path('ajax_sendSMS', views.ajax_sendSMS, name='ajax_sendSMS'),
]
