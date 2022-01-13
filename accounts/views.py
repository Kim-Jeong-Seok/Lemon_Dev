from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from .models import user
from .forms import LemonSignupForm#, SpendForm, IncomeForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# Create your views here.
import datetime
from django.db.models import Sum, Count
import os, json
from django.conf import settings
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .socialviews import KakaoSignInView, KakaoSignInCallbackView
#from .serializers import LemonUserSerializers






def main(request):

    # user_id = self.user.user_id
    # if user_id == user_id:
    #     return redirect('/calendar')

    return render(request, 'main.html')



def search_stock(request):
    return render(request, 'search_stock.html')

def stock(request):
    return render(request, 'stock.html')

def addlist(request):
    return render(request, 'addlist.html')

def myinfo(request):
    return render(request, 'myinfo.html')

def login(request):
    # 해당 쿠키에 값이 없을 경우 None을 return 한다.
    if request.COOKIES.get('username') is not None:
        username = request.COOKIES.get('username')
        password = request.COOKIES.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("calendar")
        else:
            return render(request, "alogin.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # 해당 user가 있으면 username, 없으면 None
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.POST.get("keep_login") == "TRUE":
                response = render(request, 'account/home.html')
                response.set_cookie('username',username)
                response.set_cookie('password',password)
                return response
            return redirect("home")
        else:
            return render(request, 'account/login.html', {'error':'username or password is incorrect'})
    else:
        return render(request, 'login.html')
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['password'] == request.POST['password1']:
                user = get_user_model().objects.create_user(
                                            uid=request.POST['uid'],
                                            password=request.POST['password'],
                                            email=request.POST['email'],
                                            username=request.POST['username'],
                                            phonenumber=request.POST['phonenumber'],
                                            invest=request.POST['invest'],
                                            u_chk=request.POST['u_chk'],
                                            e_chk=request.POST['e_chk'],

                                            )
                auth.login(request, user)
                # if user is not None:
                #     self.request.session['user_id'] = user_id
                #     login(self.request, user)
                #     remember_session = self.request.POST.get('remember_session', False)
                #     print('-------3333',str(remember_session))
                #     if remember_session:
                #         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                return redirect('calendar')
            return render(request, 'signup.html')
        return render(request, 'signup.html')

def user_delete(request, user_id):
    user2 = user_id
    user1 = get_user_model().objects.get(user_id = user2)
    user1.delete()
    return redirect('/')
    return render(request, 'user_delete.html')
