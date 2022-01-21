from mysettings import ALIGO_SECRET_KEY,ALIGO_USERID,ALIGO_SENDER
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import auth
from django.core import serializers
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from accounts.models import user
from .models import Income, Spend, AccountBook
from django.contrib.auth.decorators import login_required
from .calendarsforms import  SpendForm, IncomeForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# Create your views here.
import datetime,requests
from django.db.models import Sum, Count
import os, json
from django.conf import settings
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.contrib.auth.hashers import check_password
# Create your views here.
URL_LOGIN = '/login'



def detail_search(request):

    user = request.user.user_id
    start_date = request.POST.get('start_date', None)
    end_date = request.POST.get("end_date", None)
    spend_date = Spend.objects.filter(user_id = user, spend_date__range = (start_date, end_date)).values('spend_id','kind','spend_date','amount','place', 'category')
    income_date = Income.objects.filter(user_id = user, income_date__range = (start_date, end_date)).values('income_id','kind','income_date','amount','income_way', 'income_way')
    total_date = spend_date.union(income_date).order_by('-spend_date')
    print('tatal_date--->', str(total_date))

    return render(request, 'detail_search.html' , {'total_date':total_date})


def recom(request):
    return render(request, 'recom.html')

def summary(request):
    user = request.user.user_id
    now = datetime.datetime.now()
    month = now.strftime('%m')
    year = now.strftime('%Y')
    # 월별 기간 필터링
    spend_month_filter = Spend.objects.filter(user_id = user, spend_date__month=month ).values('spend_id','kind','spend_date','amount','place', 'category')
    income_month_filter = Income.objects.filter(user_id = user, income_date__month=month).values('income_id','kind','income_date','amount','income_way', 'income_way')
    # 월별 쿼리셋 합치기
    detail_month = spend_month_filter.union(income_month_filter).order_by('-spend_date')


    # 달력 일별 수입,지출값 합산
    spend_month_filter = Spend.objects.filter(user_id = user ).values('spend_id','kind','spend_date','amount','place')
    income_month_filter = Income.objects.filter(user_id = user).values('income_id','kind','income_date','amount','income_way')


    # 소비 TOP5 카테고리 , 카드, 거래처
    category_amount = spend_month_filter.values('category','card','place').annotate(amount=Sum('amount')).order_by('-amount')[:5]
    # 요약 페이지_카테고리 건수별 TOP5
    category_amount_count = spend_month_filter.values('category').annotate(count=Count('category')).order_by('-count')[:5]

    category_amount_data = []
    category_amount_label = []
    category_count_data = []
    category_count_label = []
    for item in category_amount:
        category_amount_data.append(item['amount'])
        category_amount_label.append(item['category'])
    for item in category_amount_count:
        category_count_data.append(item['count'])
        category_count_label.append(item['category'])

    return render(request, 'summary.html',
        {'month':month,
        'TOP': category_amount,
        'Category_amount_data': category_amount_data,
        'Category_amount_labels': category_amount_label,
        'Category_count_data': category_count_data,
        'Category_count_label': category_count_label,
        'Category_count': category_amount_count,})


def listview(request):

    input_year = request.POST.get('input_year', None)
    input_month = request.POST.get("input_month", None)
    user = request.user.user_id
    now = datetime.datetime.now()
    if input_year:
        year = input_year
    if input_month:
        month = input_month
    else:
        month = now.strftime('%m')
        year = now.strftime('%Y')

    # 월별 기간 필터링
    spend_month_filter = Spend.objects.filter(user_id = user, spend_date__month=month ).values('spend_id','kind','spend_date','amount','place', 'category')
    income_month_filter = Income.objects.filter(user_id = user, income_date__month=month).values('income_id','kind','income_date','amount','income_way', 'income_way')
    # 월 총 수입, 지출
    spend_sum = spend_month_filter.aggregate(Sum('amount'))
    income_sum = income_month_filter.aggregate(Sum('amount'))
    # 월별 쿼리셋 합치기
    detail_month = spend_month_filter.union(income_month_filter).order_by('-spend_date')


    spend_day_sum2 = spend_month_filter.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount')
    income_day_sum2 = income_month_filter.values('income_date__day','kind').annotate(amount=Sum('amount')).order_by('-income_date__day').values('income_date', 'kind', 'amount')

    spend_day_sum = spend_month_filter.values('spend_date__day').annotate(amount=Sum('amount')).order_by('-spend_date__day')
    income_day_sum = income_month_filter.values('income_date__day').annotate(amount=Sum('amount')).order_by('-income_date__day')

    detail_day = income_day_sum.union(spend_day_sum)

    last_spend = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_id','kind','spend_date','amount','place','category')    #.annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount')
    last_income = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_id','kind','income_date','amount','income_way','income_way')

    last_spend_sum = last_spend.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount','place')
    spend_sum = last_spend.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount','place')

    last_income_sum = last_income.values('income_date__day','kind').annotate(amount=Sum('amount')).order_by('-income_date__day').values('income_date', 'kind', 'amount')
    detail_month_sum = last_spend.union(last_income).order_by('-spend_date')

    return render(request, 'listview.html',
    {'year':year,
    'month':month,
    'Spend_day':spend_day_sum,
    'Income_day':income_day_sum,
    'Detail_month':detail_month,
    'detail_day':detail_day,
    'Expenditure': spend_sum,
    'Income': income_sum,
    # 'month':month,
    'spend_day_sum2':spend_day_sum2,
    'income_day_sum2':income_day_sum2,})

@login_required(login_url=URL_LOGIN)
def home(request):
    if request.method == 'POST':
        user = request.user.user_id
        user = get_user_model().objects.filter(user_id=user).update(
                                                u_chk=request.POST['u_chk'],
                                                e_chk=request.POST['e_chk'],
                                        )
        return redirect('/')

    return render(request, 'home.html')

@csrf_exempt
def ajax_sendSMS(request):
    if request.method == "POST":
        NUM = request.POST.get("NUM", None)
        KEY = request.POST.get("KEY", None)
    print(str(NUM)+ '그리고' + str(KEY))

    send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
    # ================================================================== 문자 보낼 때 필수 key값
    # API key, userid, sender, receiver, msg
    # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용
    sms_data={
        'key': '', #api key
        'userid': '', # 알리고 사이트 아이디
        'sender': '', # 발신번호
        'receiver': NUM, # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'[LEMON]인증번호 [{KEY}]를 입력해주세요.', #문자 내용
        #'testmode_yn' : 'Y' #테스트모드 적용 여부 Y/N
        # 'msg_type' : 'SMS', #메세지 타입 (SMS, LMS)
        # 'title' : 'testTitle', #메세지 제목 (장문에 적용)
        # 'destination' : '01000000000|고객명', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
    }
    requests.post(send_url, data=sms_data)
    data = {}

    return JsonResponse(data,safe=False)

@login_required(login_url=URL_LOGIN)
def calendar(request):
    input_year = request.POST.get('input_year', None)
    input_month = request.POST.get("input_month",None)
    user = request.user.user_id
    now = datetime.datetime.now()

    if input_year:
        year = input_year
    if input_month:
        month = input_month
    else:
        month = now.strftime('%m')
        year = now.strftime('%Y')


    # 월별 기간 필터링
    spend_month_filter = Spend.objects.filter(user_id = user, spend_date__month=month ).values('spend_id','kind','spend_date','amount','place', 'category')
    income_month_filter = Income.objects.filter(user_id = user, income_date__month=month).values('income_id','kind','income_date','amount','income_way', 'income_way')
    # 월별 쿼리셋 합치기
    detail_month = spend_month_filter.union(income_month_filter).order_by('-spend_date')


    # 달력 일별 수입,지출값 합산
    spend_month_filter = Spend.objects.filter(user_id = user ).values('spend_id','kind','spend_date','amount','place')
    income_month_filter = Income.objects.filter(user_id = user).values('income_id','kind','income_date','amount','income_way')
    spend_day_sum2 = spend_month_filter.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount')
    income_day_sum2 = income_month_filter.values('income_date__day','kind').annotate(amount=Sum('amount')).order_by('-income_date__day').values('income_date', 'kind', 'amount')
    spend_day_sum = spend_month_filter.values('spend_date__day').annotate(amount=Sum('amount')).order_by('-spend_date__day')
    income_day_sum = income_month_filter.values('income_date__day').annotate(amount=Sum('amount')).order_by('-income_date__day')

    detail_day = income_day_sum.union(spend_day_sum)

    # 월 총 수입, 지출
    spend_sum = spend_month_filter.aggregate(Sum('amount'))
    income_sum = income_month_filter.aggregate(Sum('amount'))


    #전달 내역

    input_year = request.POST.get('input_year','')
    input_month = request.POST.get("input_month",'')

    last_spend = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_id','kind','spend_date','amount','place','category')    #.annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount')
    last_income = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_id','kind','income_date','amount','income_way','income_way')

    spend_sum = last_spend.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount','place')
    #print('spend_sumspend_sumspend_sumspend_sum',str(spend_sum))
    last_income_sum = last_income.values('income_date__day','kind').annotate(amount=Sum('amount')).order_by('-income_date__day').values('income_date', 'kind', 'amount')
    detail_month_sum = last_spend.union(last_income).order_by('-spend_date')

    return render(request, 'calendar.html' ,{
        'Spend_day':spend_day_sum,
        'Income_day':income_day_sum,
        'Detail_month':detail_month,
        'detail_day':detail_day,
        'Expenditure': spend_sum,
        'Income': income_sum,

        'month':month,
        'spend_day_sum2':spend_day_sum2,
        'income_day_sum2':income_day_sum2,

        })



def add_calendar(request):
    if request.method == "POST":
        if 'spendbtn' in request.POST:
            sform = SpendForm(request.POST)
            if sform.is_valid():
                user_id = request.POST['user'],
                kind = sform.cleaned_data['kind'],
                amount = sform.cleaned_data['amount'],
                place = sform.cleaned_data['place'],
                spend_date = sform.cleaned_data['spend_date'],
                way = sform.cleaned_data['way'],
                category = sform.cleaned_data['category'],
                card = sform.cleaned_data['card'],
                memo = sform.cleaned_data['memo']
                sform.save()
                return redirect('/listview')

        elif 'incomebtn' in request.POST:
            iform = IncomeForm(request.POST)
            if iform.is_valid():
                user_id = request.POST['user'],
                kind = iform.cleaned_data['kind'],
                amount = iform.cleaned_data['amount'],
                income_date = iform.cleaned_data['income_date'],
                income_way = iform.cleaned_data['income_way'],
                memo = iform.cleaned_data['memo']
                iform.save()
                return redirect('/listview')
    else:
        sform = SpendForm()
        iform = IncomeForm()
    return render(request, 'add_calendar.html')

def edit_calendar(request, spend_id, kind):
    user = request.user.user_id
    if kind == '지출':
        spe = Spend.objects.filter(spend_id=spend_id, user_id = user)
        return render(request, 'sedit_calendar.html', {'spe':spe})
    if kind == "수입":
        income = Income.objects.filter(income_id=spend_id, user_id = user)
        return render(request, 'iedit_calendar.html', {'income':income})

def sedit_calendar(request, spend_id):
    if request.method == "POST":
        user = request.user.user_id
        spe = Spend.objects.filter(spend_id=spend_id, user_id = user).update(
        amount=request.POST['amount'],
        place = request.POST['place'],
        spend_date =request.POST['spend_date'],
        way = request.POST['way'],
        category = request.POST['category'],
        card = request.POST['card'],
        memo = request.POST['memo'])
        return redirect('/listview')

def iedit_calendar(request,spend_id):
    if request.method == "POST":
        user = request.user.user_id
        spe = Income.objects.filter(income_id=spend_id, user_id = user).update(
        kind=request.POST['kind'],
        amount = request.POST['amount'],
        income_date =request.POST['income_date'],
        income_way = request.POST['income_way'],
        memo = request.POST['memo'],)
        return redirect('/listview')

@csrf_exempt
def ajax_pushdate(request):
    if request.method == "POST":
        user = request.user.user_id
        date = request.POST.get("clikDate", None)
        spend = Spend.objects.filter(user_id = user,spend_date=date).values('kind','spend_date','amount','place')
        income = Income.objects.filter(user_id = user,income_date=date).values('kind','income_date','amount','income_way')
        detail_month = income.union(spend).order_by('kind')
        even1 = list(detail_month.values('kind','income_date','amount'))
        evens = {'msg1':even1}


        return JsonResponse(evens)

@csrf_exempt
def add_event(request):
    start = request.POST.get("start_date", None)
    end = request.POST.get("start_date", None)
    title = request.POST.get("title", None)
    print(str(start))
    event = Please(
            title=str(title),
            start="%s(start)", end="%s(end)")
    event.save()
    data = {}
    return JsonResponse(data)

def all_events(request):
    all_events = Please.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.title,
            'start': event.start_date,
            'end': event.end_date,
        })

    return JsonResponse(out, safe=False)

@csrf_exempt
def load_list(request):
    if request.method == "POST":
        user = request.user.user_id
        #date = request.POST.get('date')

        #print('month_input',str(month_input))
        #print('유저id->>' + str(user) +'이 작성한' + str(month_input) + '를 가져옵니다.')
        date2 = month_input.split('-')
        year = date2[0]
        month = date2[1]
        #print('month',str(month))
        # year = 2021
        # month = 12

        spend = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_id','kind','spend_date','amount','place','category')    #.annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount')

        income = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_id','kind','income_date','amount','income_way','income_way')

        spend_sum = spend.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount','place')
        #print('spend_sumspend_sumspend_sumspend_sum',str(spend_sum))
        income_sum = income.values('income_date__day','kind').annotate(amount=Sum('amount')).order_by('-income_date__day').values('income_date', 'kind', 'amount')
        detail_month = spend.union(income).order_by('-spend_date')
        #print('spend_sumspend_sum',str(spend_sum))
        #print('income_sumincome_sum',str(income_sum))
        # spend_day_sum = spend_month_filter.values('spend_date__day').annotate(amount=Sum('amount')).order_by('-spend_date__day')
        # income_day_sum = income_month_filter.values('income_date__day').annotate(amount=Sum('amount')).order_by('-income_date__day')
        # 월별 쿼리셋 합치기
        #detail_month = spend.union(income).order_by('-spend_date')
        #print(detail_month)
        # data2 = list(detail_month)
        # data3 = list(spend_sum)
        # data4 = list(income_sum)
        return redirect('calendar')
        #return render(request, 'calendar.html', {'detail':detail_month})
        #print(data2)
    # return JsonResponse({"data2":data2,"data3":data3,"data4":data4})
