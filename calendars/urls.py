from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .models import Income, Spend, AccountBook
from django.conf.urls import include



app_name = 'calendars'

urlpatterns = [


    path('calendar', views.calendar, name='calendar'),
    # path('cal', views.cal, name='cal'),
    #path('cal_list', views.cal_list, name='calendarList'),

    # path('addlist', views.addlist, name='addlist'),
    #path('addlist', views.addlist, name='addlist'),
    path('add_calendar/', views.add_calendar, name='add_calendar'),
    # path('invest', views.invest, name='invest'), #모의주식금액설정
    path('edit_calendar/<str:kind>/<int:spend_id>/', views.edit_calendar, name='edit_calendar'),
    #path('edit_calendar/<int:income_id>/<str:kind>/', views.edit_calendar, name='edit_calendar'),
    #path('user_delete/<int:user_id>', views.user_delete, name='user_delete'), #회원탈퇴

    path('add_calendar', views.add_calendar, name='add_calendar'),
    path('ajax_pushdate/', views.ajax_pushdate, name='ajax_pushdate'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event', views.add_event, name='add_event'),
]
