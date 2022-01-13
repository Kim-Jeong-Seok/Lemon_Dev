ibbfrom django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from accounts.models import user
from .models import Income, Spend, AccountBook
from django.db.models import FloatField
from django.db.models.functions import Cast, TruncMonth, TruncDate
from itertools import groupby
from operator import attrgetter
from .calendarsforms import  SpendForm, IncomeForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# Create your views here.
import datetime
from django.db.models import Sum, Count, Max, Min, Avg
import os, json
from django.conf import settings
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers


from django.contrib.auth.hashers import check_password
# Create your views here.




def calendar(request):
    if request.method == 'POST':
        user = request.user.user_id
        user = get_user_model().objects.filter(user_id=user).update(
                                            u_chk=request.POST['u_chk'],
                                            e_chk=request.POST['e_chk'],
                                    )
        return redirect('/calendar#recom')


    user = request.user.user_id
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
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


    return render(request, 'calendar.html' ,{
        'Spend_day':spend_day_sum,
        'Income_day':income_day_sum,
        'Detail_month':detail_month,
        'detail_day':detail_day,
        'Expenditure': spend_sum,
        'Income': income_sum,
        'TOP': category_amount,
        'month':month,
        'spend_day_sum2':spend_day_sum2,
        'income_day_sum2':income_day_sum2,
        'Category_amount_data': category_amount_data,
        'Category_amount_labels': category_amount_label,
        'Category_count_data': category_count_data,
        'Category_count_label': category_count_label,
        'Category_count': category_amount_count,
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
                return redirect('/calendar#list')

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
                return redirect('/calendar#list')
    else:



        sform = SpendForm()
        iform = IncomeForm()
    return render(request, 'add_calendar.html')

def edit_calendar(request, spend_id, kind):

    user = request.user.user_id

    if kind == '지출':)
        spe = Spend.objects.filter(spend_id=spend_id, user_id = user)
        #return redirect('/calendar#list')
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
        return redirect('/calendar#list')

def iedit_calendar(request,spend_id):
    if request.method == "POST":
        user = request.user.user_id
        spe = Income.objects.filter(income_id=spend_id, user_id = user).update(
        kind=request.POST['kind'],
        amount = request.POST['amount'],
        income_date =request.POST['income_date'],
        income_way = request.POST['income_way'],
        memo = request.POST['memo'],)
        return redirect('/calendar#list')




@csrf_exempt
def ajax_pushdate(request):
    if request.method == "POST":
        user = request.user.user_id
        test = request.POST.get("testtest", None)
        spend = Spend.objects.filter(user_id = user,spend_date=test).values('kind','spend_date','amount','place')
        income = Income.objects.filter(user_id = user,income_date=test).values('kind','income_date','amount','income_way')
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
        year = request.POST.get("year",None)
        month = request.POST.get("month",None)
        json_year = json.loads(year)
        json_month = json.loads(month)
        print('year month->>' + str(json_year) + str(json_month))


        spend = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_date__day').annotate(Count('spend_date')).values('spend_id','kind','spend_date','amount','place','category')
        print("spend spendspend : ", str(spend))
        income = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_date__day').annotate(Count('income_date')).values('income_id','kind','income_date','amount','income_way','income_way')
        print("income incomeincome : ", str(income))
        # 월별 쿼리셋 합치기
        detail_month = spend.union(income).order_by('spend_date')
        print("detail_month detail_month : ", str(detail_month))
        detail_month = list(detail_month)
        #detail_month = {'detail_month':detail_month }
        return JsonResponse(detail_month, safe=False)
        #return render(request, 'calendar.html' , context)

        # detail_month = list(detail_month)
        # print("Dictionary Type : ", type(detail_month))('spend_id','kind','spend_date','amount','place','category')
        #return JsonResponse(detail_month, safe=False)



# @csrf_exempt
# def load_list(request):
#     if request.method == "POST":
#         user = request.user.user_id
#         year = request.POST.get('year')
#         month = request.POST.get('month')
#         json_year = json.loads(year)
#         json_month = json.loads(month)
#         print('year month->>' + str(json_year) + str(json_month))
#
#         spend = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_id','kind','spend_date','amount','place','category')
#
#         income = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_id','kind','income_date','amount','income_way','income_way')
#         # 월별 쿼리셋 합치기
#
#         detail_month = spend.union(income).order_by('-spend_date')
#         print("Dictionary Type : ", type(detail_month))
#         detail_month = list(detail_month)
#
#         print("Dictionary Type : ", type(detail_month))
#
#         a = {'detail_month':detail_month}
#
#         detail_month1 = dict(a)
#
#         print("Dictionary Type : ", type(detail_month))
#         #return render(request, 'calendar.html' , dict(detail_month1))
#         return JsonResponse(detail_month, safe=False)


    #     print("Dictionary : ", detail_month)
    #     detail_month = dict(detail_month)
    #     print(str(detail_month))
    # return JsonResponse(detail_month, safe=False)
    # return render(requset, cdetail_month, safe=False)
    #return render(request, 'calendar.html' , dict(detail_month1 ))
# @csrf_exempt
# def load_list(request):
#     if request.method == "POST":
#         user = request.user.user_id
#         year = request.POST.get('year')
#         month = request.POST.get('month')
#         print(str(month + year))
#         json_year = json.loads(year)
#         json_month = json.loads(month)
#         year = json_year
#         month = json_month
#         spend = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_id','kind','spend_date','amount','place','category')
#         income = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_id','kind','income_date','amount','income_way','income_way')
#         # 월별 쿼리셋 합치기
#         detail_month = spend.union(income).order_by('-spend_date')
#         detail_month = list(detail_month)
#
#         detail_month2 = list(detail_month)
#
#         print("Dictionary Type : ", type(detail_month))
#
#         # a = {'detail_month':detail_month}
#
#         detail_month3 = dict(detail_month2)
#
#         print("Dictionary Type : ", type(detail_month))
#
#         print("Dictionary : ", detail_month)
#         de = dict(detail_month)
#         return JsonResponse(de, safe=False)
#         return render(request, 'calendar.html' , dict(detail_month3))
    #return JsonResponse(detail_month)
    # return render(request, 'load_list' , dict(detail_month3=detail_month3))
