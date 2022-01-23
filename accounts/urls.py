from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

#from .views import LemonUserAPI
app_name='accounts'

urlpatterns = [
    path('main', views.main, name='main'),
    path('search_stock', views.search_stock, name='search_stock'),
    path('stock', views.stock, name='stock'),
    path('addlist', views.addlist, name='addlist'),
    path('myinfo', views.myinfo, name='myinfo'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_delete/<int:user_id>', views.user_delete, name='user_delete'), #회원탈퇴
    path('notice', views.notice, name='notice'), # 공지사항
    path('notice/<int:pk>', views.notice_detail, name='notice_detail'), # 공지사항 상세보기
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)