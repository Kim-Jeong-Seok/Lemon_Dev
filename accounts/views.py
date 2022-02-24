import email
from unittest import result
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from .models import user
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime, date, timedelta
from django.db.models import Sum, Count
import os, json
from django.conf import settings
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .socialviews import KakaoSignInView, KakaoSignInCallbackView
from django.urls import reverse_lazy
from django.core.mail.message import EmailMessage
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

# Create your views here.

URL_LOGIN = '/login'

def send_email(request):
    subject = "message"
    to = ["limjs2671@gmail.com"]
    from_email = "basoup.t@gmail.com"
    message = "메지시 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()


def policy(request):
    return render(request, 'policy.html')

def main(request):
    return render(request, 'main.html')

@login_required(login_url=URL_LOGIN)
def myinfo(request):
    return render(request, 'myinfo.html')

def find_id(request):
    return render(request, 'find_id.html')

def find_id_result(request):
    if request.method == "POST":
        find_email = request.POST.get('find_email', None)
        result = get_user_model().objects.filter(email = find_email).values_list('uid', flat=True)
        if result.exists():
            result = result
        else:
            result = 0
    return render(request, 'find_id_result.html', {'result':result})

def signup(request):
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber', None)
        phonenumber = str(phonenumber)
        invest = request.POST['invest']
        birthday = request.POST['birthday']
        pin = request.POST['pin']
        if invest == '0':
            #invest_date = None
            invest_date = date(1111,1,11)
        else:
            invest_date = datetime.now()

        if birthday == '':
            #birthday = date(1111, 1, 11)
            birthday = datetime.now()
        else:
            birthday = birthday

        if pin == '':
            pin = '0000'
            pin_date = datetime.now() + timedelta(hours=12)
        else:
            pin = pin
            pin_date = datetime.now() + timedelta(hours=12)
        if request.POST['password'] == request.POST['password1']:
            user = get_user_model().objects.create_user(
                                            uid=request.POST['uid'],
                                            password=request.POST['password'],
                                            username=request.POST['username'],
                                            gender=request.POST['gender'],
                                            job=request.POST['job'],
                                            email=request.POST['email'],
                                            phonenumber=phonenumber,
                                            invest=request.POST['invest'],
                                            invest_date=invest_date,
                                            u_chk=request.POST['u_chk'],
                                            pin = pin,
                                            pin_date=pin_date,
                                            birthday = birthday,
                                            )
            auth.login(request, user)
            return redirect('/home')
        return render(request, 'signup.html')
    return render(request, 'signup.html')


def pin_date_save(request):
    now_time = datetime.now() + timedelta(days=1)
    if request.method == 'POST':
        user_id = request.user.user_id
        user_db = user.objects.get(user_id=user_id)
        user_db.pin_date = now_time
        user_db.save()
        return redirect('/home')


class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  # 템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        if user.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'registration/password_reset_done_fail.html')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력


def fail(request):
    return render(request, 'registration/password_reset_done_fail.html')

def ajax_checkID(request):
    if request.method == "POST":
        uid = request.POST.get('Vaildid', None)

        id = user.objects.filter(uid=uid).values('uid')
        if id:
            result_msg = 0
        else:
            result_msg = 1

        return JsonResponse(result_msg, safe=False)


def ajax_checkEmail(request):
    if request.method == "POST":
        vailEmail = request.POST.get('vailEmail', None)

        email = user.objects.filter(email=vailEmail).values('email')
        if email:
            result_msg = 0
        else:
            result_msg = 1

        return JsonResponse(result_msg, safe=False)


# 소셜 로그인 추가정보 입력
def social_info(request):
    u_check = request.user.u_chk
    if u_check == False:
    
        if request.method == 'POST':
            user = request.user.user_id
            phonenumber = request.POST.get('phonenumber', None)
            phonenumber = str(phonenumber)
            invest = request.POST['invest']
            birthday = request.POST['birthday']
            pin = request.POST['pin']

            if invest == '0':
                #invest_date = None
                invest_date = date(1111,1,11)
            else:
                invest_date = datetime.now()

            if birthday == '':
                #birthday = date(1111, 1, 11)
                birthday = datetime.now()
            else:
                birthday = birthday
            if pin :
                pin = pin
                pin_date = datetime.now() + timedelta(hours=12)

            user = get_user_model().objects.filter(user_id=user).update(
                u_chk=request.POST['u_chk'],
                username=request.POST['username'],
                email=request.POST['email'],
                gender=request.POST.get("gender"),
                job=request.POST.get("job"),
                phonenumber=phonenumber,
                birthday=birthday,
                pin=pin,
                pin_date=pin_date,
                invest=invest,
                invest_date=invest_date,
            )
            return redirect('/home')
    else:
        return redirect('/home')
    return render(request, 'social_signup-aditional_info.html') 