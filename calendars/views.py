from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from accounts.models import user
from .models import Income, Spend, AccountBook

from .calendarsforms import  SpendForm, IncomeForm
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
    # events = AccountBook.objects.filter(user_id=user )
    # income = Income.objects.filter(user_id=user)
    # spend = Spend.objects.filter(user_id=user)
    events = Income.objects.all().values("amount", "income_date" ,"kind").union(Spend.objects.all().values("amount","spend_date", "kind"))
    total = AccountBook.objects.all().values_list("account_date").union()

    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')

    # 월별 기간 필터링
    spend_month_filter = Spend.objects.filter(user_id = user,spend_date__year=year, spend_date__month=month).values('kind','spend_date','amount','place')
    income_month_filter = Income.objects.filter(user_id = user,income_date__year=year, income_date__month=month).values('kind','income_date','amount','income_way')
    # 월별 쿼리셋 합치기
    detail_month = spend_month_filter.union(income_month_filter).order_by('-spend_date')
    # 일별 수입,지출값 합산
    spend_day_sum2 = spend_month_filter.values('spend_date__day','kind').annotate(amount=Sum('amount')).order_by('-spend_date__day').values('spend_date', 'kind', 'amount')
    income_day_sum2 = income_month_filter.values('income_date__day','kind').annotate(amount=Sum('amount')).order_by('-income_date__day').values('income_date', 'kind', 'amount')

    spend_day_sum = spend_month_filter.values('spend_date__day').annotate(amount=Sum('amount')).order_by('-spend_date__day')
    income_day_sum = income_month_filter.values('income_date__day').annotate(amount=Sum('amount')).order_by('-income_date__day')

    detail_day = income_day_sum.union(spend_day_sum)


    # 월별 기간 필터링
    spend_month_filter2 = Spend.objects.filter(user_id = user, spend_date__year=year, spend_date__month=month)
    income_month_filter2 = Income.objects.filter(user_id = user, income_date__year=year, income_date__month=month)
    # 월 총 수입, 지출
    spend_sum = spend_month_filter2.aggregate(Sum('amount'))
    income_sum = income_month_filter2.aggregate(Sum('amount'))
    # 소비 TOP5 카테고리
    category_amount = spend_month_filter2.values('category').annotate(amount=Sum('amount')).order_by('-amount')[:5]
    # 소비 TOP5 카드
    method_amount = spend_month_filter2.values('card').annotate(amount=Sum('amount')).order_by('-amount')[:5]
    # 소비 TOP5 거래처
    area_amount = spend_month_filter2.values('place').annotate(amount=Sum('amount')).order_by('-amount')[:5]
    # 요약 페이지_카테고리 건수별 TOP5
    category_amount_count = spend_month_filter2.values('category').annotate(count=Count('category')).order_by('-count')[:5]


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
        'events':events,
        'Expenditure': spend_sum,
        'Income': income_sum,
        'Category': category_amount,
        'Method': method_amount,
        'Area': area_amount,
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
                return redirect('/calendar#calendar')

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
                return redirect('/calendar#calendar')
    else:
        sform = SpendForm()
        iform = IncomeForm()
    return render(request, 'add_calendar.html')

@csrf_exempt
def ajax_pushdate(request):
    if request.method == "POST":
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