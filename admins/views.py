from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from accounts.models import user
from .models import Notice, Faq
from datetime import timedelta
from datetime import datetime
from django.http import JsonResponse
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
    can_date = user_db.invest_date + timedelta(days=30) if user_db.invest_date else 0000-00-00
    if request.method == "POST":
        input_money = request.POST.get("input_money", None)
        uid = int(input_money)
        user_db.invest_date = now_date
        user_db.invest = uid + user_db.invest
        user_db.save()
        data = {}
        return JsonResponse(data)
    return render(request, 'invest.html', {'user': user_db, 'can_date': can_date, 'now_date': now_date})

# 내 정보 변경
def edit_myinfo(request):
    if request.method == 'POST':
        user_id = request.user.user_id
        user_db = user.objects.get(user_id=user_id)
        user_db.username = request.POST['username']
        user_db.gender = request.POST['gender']
        user_db.job = request.POST['job']
        user_db.birthday = request.POST['birthday']
        #user_db.phonenumber = request.POST['phonenumber']
        user_db.save()
        return redirect('/myinfo/update')
    return render(request, 'edit_myinfo.html')

# 전화번호 변경
def changephone(request):
    if request.method == "POST":
        phonenumber = request.POST.get('phonenumber')
        phonenumber = str(phonenumber)
        user_id = request.user.user_id
        user_db = user.objects.get(user_id=user_id)
        user_db.phonenumber = phonenumber
        user_db.save()
        return redirect('/myinfo/update')
    return render(request, 'changephone.html')

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
    return redirect('/login')
    return render(request, 'user_delete.html')

# FAQ(자주 묻는 질문)
def faq(request):
    faq = Faq.objects.all().order_by('-faq_id')
    return render(request, 'faq.html', {'faqs': faq})

# FAQ 상세보기
def faq_detail(request, pk):
    faq = Faq.objects.get(faq_id = pk)
    return render(request, 'faq_detail.html', {'faq': faq})

# SMS 읽기
def sms_read(request):
    return render(request, 'sms_read.html')

# 문자내역 지출작성 페이지
def sms_write(request):
    return render(request, 'sms_write.html')
