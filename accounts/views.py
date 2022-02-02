from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from .models import user
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
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

URL_LOGIN = '/login'

def main(request):
    return render(request, 'main.html')

@login_required(login_url=URL_LOGIN)
def myinfo(request):
    return render(request, 'myinfo.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password1']:
            user = get_user_model().objects.create_user(
                                            uid=request.POST['uid'],
                                            password=request.POST['password'],
                                            username=request.POST['username'],
                                            gender=request.POST['gender'],
                                            job=request.POST['job'],
                                            email=request.POST['email'],
                                            phonenumber=request.POST['phonenumber'],
                                            invest=request.POST['invest'],
                                            u_chk=request.POST['u_chk'],
                                            pin=request.POST['pin'],
                                            birthday=request.POST['birthday'],
                                            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')
