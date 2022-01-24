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
    path('summary', views.summary, name='summary'), # 요약페이지
    path('recom', views.recom, name='recom'), # 추천페이지
    path('list_view', views.list_view, name='list_view'), # 내역페이지
    #path('calendar', views.list, name='list'),
    # path('cal_list', views.cal_list, name='calendarList'),

    # path('addlist', views.addlist, name='addlist'),

    path('add_calendar/', views.add_calendar, name='add_calendar'),
    path('edit_calendar/<str:kind>/<int:spend_id>/', views.edit_calendar, name='edit_calendar'),
    path('sedit_calendar/<int:spend_id>', views.sedit_calendar, name='sedit_calendar'),
    path('iedit_calendar/<int:spend_id>', views.iedit_calendar, name='iedit_calendar'),
    # path('invest', views.invest, name='invest'), #모의주식금액설정

    path('ajax_pushdate/', views.ajax_pushdate, name='ajax_pushdate'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event', views.add_event, name='add_event'),
    path('load_list', views.load_list, name='load_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)