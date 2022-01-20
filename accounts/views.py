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
#from .socialviews import KakaoSignInView, KakaoSignInCallbackView
from allauth.socialaccount.providers.kakao import views as kakao_view
from mysettings import SECRET_KEY,KAKAO_KEY
from django.views import View


URL_LOGIN = '/login'


class KakaoSignInView(View):
    def get(self, request):
        client_id = KAKAO_KEY['KAKAO_KEY']
        redirect_uri = 'http://127.0.0.1:8000/account/kakao/login/callback/'
        #redirect_uri = "https://192.168.0.26:8000/account/kakao/login/callback/"
        kakao_auth_api = 'http://kauth.kakao.com/pauth/author?response_type=code '
        return redirect(
                f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={'http://127.0.0.1:8000/account/kakao/login/'}&response_type=code"
            )

class KakaoSignInCallbackView(View):
    def get(self, request):
        try:
            code            = request.GET.get("code")
            client_id       = KAKAO_KEY['KAKAO_KEY']
            redirect_uri    = "http://127.0.0.1:8000/account/kakao/login/callback/"
            #redirect_uri = "https://192.168.0.26:8000/account/kakao/login/callback/"
            token_request   = requests.get(
                f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
            )
            token_json      = token_request.json()
            #print(token_json)

            error           = token_json.get("error", None)

            if error is not None:
                return JsonResponse({"message":"INVALD_CODE"}, status=400)

            access_token    = token_json.get("access_token")

            profile_request     = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
            )

            profile_json        = profile_request.json()
            kakao_account       = profile_json.get("kakao_account")
            email               = kakao_account.get("email", None)
            kakao_id            = profile_json.get("id")
            profileImageUR      = profile_json.get("profile_image")
            nickName            = profile_json.get("nickname")


        except KeyError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)

        except access_token.DoesNotExist:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)
        if member.objects.filter(social_account = kakao_id).exists():
            kakao_user    = member.objects.get(social_account = kakao_id)
            token   = jwt.encode({"email":email}, SECRET['SECRET_KEY'], algorithm="HS256")
            token   = token.decode("utf-8")

            print("success")

            return JsonResponse({"token" : token}, status=200)


        else:
            member(social_account = kakao_id,
                email    = email,
            ).save()
            token = jwt.encode({"email" : email}, SECRET['SECRET_KEY'], algorithm = "HS256")
            token = token.decode("utf-8")
            return JsonResponse({"token" : token}, status = 200)
def main(request):
    return render(request, 'main.html')


def search_stock(request):
    return render(request, 'search_stock.html')

@login_required(login_url=URL_LOGIN)
def stock(request):
    return render(request, 'stock.html')

@login_required(login_url=URL_LOGIN)
def addlist(request):
    return render(request, 'addlist.html')

@login_required(login_url=URL_LOGIN)
def myinfo(request):
    return render(request, 'myinfo.html')

def signup(request):
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
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def user_delete(request, user_id):
    user2 = user_id
    user1 = get_user_model().objects.get(user_id = user2)
    user1.delete()
    return redirect('/')
    return render(request, 'user_delete.html')
