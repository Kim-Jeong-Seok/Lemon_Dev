from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from calendars import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'calendars'

urlpatterns = [

    path('home', views.home, name='home'),
    path('top5', views.top5, name='top5'),
    path('summary', views.summary, name='summary'), # 요약페이 지
    path('recom', views.recom, name='recom'), # 추천페이지
    path('history', views.history, name='history'), # 내역페이지
    path('detail_search', views.detail_search, name='detail_search'), # 내역필터페이지
    path('sms_add_spend_calendar/<str:date>/<int:amount>/<str:place>', views.sms_add_spend_calendar, name='sms_add_spend_calendar'),  # SMS문자내역 입력
    path('add_income_calendar/', views.add_income_calendar, name='add_income_calendar'),
    path('add_spend_calendar/', views.add_spend_calendar, name='add_spend_calendar'),
    path('sms_add_spend_calendar/', views.sms_add_spend_calendar, name='sms_add_spend_calendar'), # SMS문자내역 입력
    path('edit_calendar/<str:kind>/<int:spend_id>/', views.edit_calendar, name='edit_calendar'),
    path('sedit_calendar/<int:spend_id>', views.sedit_calendar, name='sedit_calendar'),
    path('iedit_calendar/<int:income_id>', views.iedit_calendar, name='iedit_calendar'),
    path('category_detail/<int>', views.category_detail, name= 'category_detail'),
    path('delete_shistory/<int:spend_id>', views.delete_shistory, name='delete_shistory'),
    path('delete_ihistory/<int:income_id>', views.delete_ihistory, name='delete_ihistory'),
    path('spend_search_result', views.spend_search_result, name='spend_search_result'),

    path('ajax_pushdate', views.ajax_pushdate, name='ajax_pushdate'),
    path('ajax_sendSMS', views.ajax_sendSMS, name='ajax_sendSMS'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)