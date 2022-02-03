from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from accounts.models import user
from .models import Notice
from datetime import timedelta
from datetime import datetime
from django.contrib.auth import login, authenticate, get_user_model
# Create your views here.

#  문의하기
def qna(request):
    return render(request, 'qna.html')

# 공지사항
def notice(request):
    notice = Notice.objects.all().order_by('-notice_id')
    return render(request, 'notice.html', {'notices': notice})

# 공지사항 상세보기
def notice_detail(request, pk):
    notice = Notice.objects.get(notice_id = pk)
    return render(request, 'notice_detail.html', {'notice': notice})

# 자산 설정
def invest_change(request):
    user_id = request.user.user_id
    user_db = user.objects.get(user_id=user_id)
    previous_date = user_db.invest_date
    now_date = datetime.now()
    can_date = user_db.invest_date + timedelta(days=30)
    # try:
    #     if((previous_date.strftime('%Y %m')) == (now_date.strftime('%Y %m'))): # 당월 중복변경의 경우 myinfo로 이동
    #         return render(request, 'myinfo.html', {'message': '변경불가'})
    #     else: # 당월 첫변경의 경우 invest로 이동
    #         if request.method == 'POST':
    #             user_db.invest_date = now_date
    #             user_db.invest = request.POST['invest']
    #             user_db.save()
    #             return redirect('/myinfo')
    # except AttributeError:
    if request.method == 'POST':
            user_db.invest_date = now_date
            user_db.invest = request.POST['invest']
            user_db.save()
            return redirect('/invest/update')
    return render(request, 'invest.html', {'user': user_db, 'can_date': can_date, 'now_date': now_date})

# 내 정보 변경
def edit_myinfo(request):
    if request.method == 'POST':
        user_id = request.user.user_id
        user_db = user.objects.get(user_id=user_id)
        user_db.username = request.POST['username']
        user_db.phonenumber = request.POST['phonenumber']
        user_db.save()
        return redirect('/myinfo/update')
    return render(request, 'edit_myinfo.html')

# pin번호
def input_pin(request):
    if request.method == 'POST':
        user_id = request.user.user_id
        user_db = user.objects.get(user_id=user_id)
        user_db.pin = request.POST['pin']
        user_db.save()
        return redirect('/myinfo')
    return render(request, 'input_pin.html')

# 회원탈퇴
def user_delete(request, user_id):
    user2 = user_id
    user1 = get_user_model().objects.get(user_id = user2)
    user1.delete()
    return redirect('/')
    return render(request, 'user_delete.html')
