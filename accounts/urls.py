from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

#from .views import LemonUserAPI
app_name='accounts'

urlpatterns = [
    path('', views.main, name='main'),
    path('myinfo', views.myinfo, name='myinfo'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('authaccounts/kakao/login', views.KakaoSignInView, name='KakaoSignInView'),
    path('send_email', views.send_email, name='send_email'),
    path('pin_date_save', views.pin_date_save, name='pin_date_save'),
    path('policy', views.policy, name='policy'),

    path('find_id', views.find_id, name='find_id'),
    path('find_id_result', views.find_id_result, name='find_id_result'),

    path('accounts/password_reset/',views.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('fail', views.fail, name='fail'),

    path('ajax_checkID/', views.ajax_checkID, name="ajax_checkID"),  # 아이디중복 체크
    path('ajax_checkEmail/', views.ajax_checkEmail, name="ajax_checkEmail"),  # 이메일 중복 체크
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)