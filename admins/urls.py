from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='admins'

urlpatterns = [
    path('qna', views.qna, name='qna'), # 문의하기
    path('notice', views.notice, name='notice'), # 공지사항
    path('notice/<int:pk>', views.notice_detail, name='notice_detail'), # 공지사항 상세보기
    path('invest/update', views.invest_change, name='edit_invest'), # 자산 설정
    path('myinfo/update', views.edit_myinfo, name='edit_myinfo'), # 내 정보 변경
    path('pin/input', views.input_pin, name='input_pin'), # pin번호 변경
    path('user_delete/<int:user_id>', views.user_delete, name='user_delete'), #회원탈퇴

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
