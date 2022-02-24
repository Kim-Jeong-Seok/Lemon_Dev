from django.shortcuts import render, redirect

# Create your views here.
import json
from django.http import JsonResponse
from datetime import datetime
from django.db import transaction
from . import kocom
from . import iex
from . import stockcal as cal
from .models import *
from accounts import models as acc_models
from stocks.models import Stocksector
from django.db.models import Sum, Count, F
from decimal import *

def search_stock(request):
    wntlr = Totalmerge.objects.all().values('id', 'name')
    return render(request, 'search_stock.html', {'wntlr': wntlr})


def stock(request):
    stockheld = Stockheld.objects.filter(sh_userid=request.user.user_id).exclude(sh_share=0) # 자기가 구매한 것 보이고 다 판건 안보이게 만듬
    stock_data = []
    stock_cal = cal.calculator()
    koscom_api = kocom.api()
    mark = bookmark.objects.filter(user_id=request.user.user_id)
    bookmark_date = []
    for element in stockheld:
        average_price = stock_cal.average_price(request.user.user_id, element.sh_isusrtcd)
        current_price = koscom_api.get_current_price(element.sh_marketcode, element.sh_isusrtcd)
        stock_data.append(
            [element.sh_isukorabbrv, average_price, current_price, element.sh_isusrtcd, element.sh_marketcode, element.sh_share])

    for element in mark :
        find_stock_name = Stocksector.objects.filter(ss_isusrtcd=element.isuSrtCd).values_list('ss_isukorabbrv', flat=True)
        name = find_stock_name[0]
        current_price = koscom_api.get_current_price(element.marketcode, element.isuSrtCd)
        bookmark_date.append([element.marketcode,element.isuSrtCd, current_price, name])
    return render(request, 'stock.html', {'stock_data': stock_data,'bookmark_date':bookmark_date})

def suggestion(request):
    koscom_api = kocom.api()
    nasdaq_api = iex.api()
    categorys = Stockheld.objects.exclude(sh_share=0).filter(sh_userid=request.user.user_id ).values('sh_idxindmidclsscd', 'sh_isusrtcd').annotate(count=Count('sh_idxindmidclsscd')).order_by('-count').distinct()
    category_list = list(categorys.values('sh_idxindmidclsscd'))
    categorys_isurtcd = list(categorys.values('sh_isusrtcd'))
    category_keep = category_list[0:3]
    category_arr = []
    isurtcd_arr = []
    for i in category_keep:
        category_arr.append(i['sh_idxindmidclsscd'])
    for i in categorys_isurtcd:
        isurtcd_arr.append(i['sh_isusrtcd'])
    #stock_list = Category.objects.select_related('spend').filter(category=4)
    stock_suggestion1 = Totalmerge.objects.exclude(id__in=isurtcd_arr).filter(category__in=category_arr[0:3]).values("id", 'per', 'pbr', "marketcode", "name", "category").annotate(
        ROA=(F('per') * Decimal('1.0') / F('pbr') * Decimal('1.0'))).order_by('-ROA')[0:5]
    print(stock_suggestion1)
    #stock_suggestion2 = list(stock_suggestion1)
    category_stock = []

    for element in stock_suggestion1:
        issuecode = element['id']
        stock_suggestion = koscom_api.get_current_price(element['marketcode'], issuecode)
        print(stock_suggestion)
        category_stock.append([stock_suggestion, issuecode, element['per'],
                              element['pbr'], element['marketcode'], element['name'], element['category']])
        print(category_stock)
    nasdaq_category = nasdaq_test.objects.filter(category__in=category_arr[0:3]).values_list('nasdaq_cname', flat=True).values("nasdaq_cname")
    print(nasdaq_category)
    nasdaq_top5 = Totalmerge.objects.exclude(id__in=isurtcd_arr).filter(category__in=nasdaq_category).values("id", 'per', 'pbr', "marketcode", "name", "category").annotate(ROA=(F('per') * Decimal('1.0') / F('pbr') * Decimal('1.0'))).order_by('-ROA')[0:5]
    print(nasdaq_top5)
    nasdaq_top5_price = []


    for element in nasdaq_top5:
        symbol = element['id']
        print(symbol)
        # marketcode = element['marketcode']
        # print(marketcode)
        naqdaq_price = nasdaq_api.get_current_price(element['marketcode'],symbol)
        print(naqdaq_price)
        nasdaq_top5_price.append([naqdaq_price, element['id'], element['per'],
                                element['pbr'], element['marketcode'], element['name'], element['category']])
        print(nasdaq_top5_price)

    # result = {}
    # result['category_stock'] = category_stock
    # result['nasdaq_top5_price'] = nasdaq_top5_price
    # print(result)

    return render(request, 'suggestions.html', {'category_stock':category_stock, 'nasdaq_top5_price':nasdaq_top5_price })

def portfolio(request):
    result = {}
    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
    total = total_use_investment_amount - total_investment_amount
    user_total_investment_amount = stock_cal.user_total_investment_amount(request.user.user_id)

    total = total_use_investment_amount - total_investment_amount
    total_current_price = stock_cal.total_current_price(request.user.user_id)
    total_use_investment_amount = stock_cal.total_use_investment_amount(
        request.user.user_id)
    invest = request.user.invest
    total_invest = invest + total_use_investment_amount

    user_total_investment_amount = stock_cal.user_total_investment_amount(request.user.user_id)
    print('----B,S 포함한 총가격--------')
    print(user_total_investment_amount)

    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    print('-------    # 현재 있는 주식에 대한 전체 구매한 양-----')
    print(total_investment_amount)

    total_current_price = stock_cal.total_current_price(request.user.user_id)
    print('-----    # 현재 있는 주식에 대한 전체 현재가-------')
    print(total_current_price)
    # total_user = total_investment_amount -user_total_investment_amount
    # print('-----  total_investment_amount -user_total_investment_amount  # -------')
    # print(total_user)

    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
    print('------총손익금------')
    print(total_investment_amount + total_use_investment_amount)
    invest = request.user.invest
    total_invest = invest + total_use_investment_amount
    print(total_invest)


    if total_investment_amount is False or total_current_price is False or total_use_investment_amount is False or user_total_investment_amount is False:
        result['total_investment_amount'] = 0
        result['user_total_investment_amount'] = 0
        result['total_current_price'] = 0
        result['total_use_investment_amount'] = 0
        result['total_invest'] = 0
        result['total'] = total
    else:
        result['total'] = total
        result['user_total_investment_amount'] = user_total_investment_amount
        result['total_investment_amount'] = total_investment_amount
        result['total_current_price'] = total_current_price
        result['total_use_investment_amount'] = total_use_investment_amount
        result['total_invest'] = total_invest
    print(invest)
    print(total_investment_amount)
    print(total_use_investment_amount)
    return render(request, 'portfolio.html', result)


def stock_info(request, marketcode, issuecode):
    api = iex.api() if marketcode == 'nasdaq' else kocom.api()
    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
    result = api.get_current_stock(marketcode, issuecode) if marketcode == 'nasdaq' else api.get_stock_master(marketcode, issuecode)
    mark = bookmark.objects.filter(user_id=request.user.user_id, marketcode=marketcode, isuSrtCd=issuecode)
    if mark:
        star=1
    else :
        star=0
    if result:
        result['total_investment_amount'] = total_investment_amount if total_investment_amount else 0
        result['total_use_investment_amount'] = total_use_investment_amount if total_use_investment_amount else 0
        result['total'] = result['total_use_investment_amount'] - result['total_investment_amount']
        result['share'] = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                   sh_isusrtcd=issuecode).values_list('sh_share', flat=True)
        result['curPrice'] = api.get_current_price(marketcode, issuecode)
        result['marketcode'] = marketcode
        result['total_allow_invest'] = request.user.invest - stock_cal.total_use_investment_amount(request.user.user_id)

        if marketcode == 'nasdaq':
            result['year_history'] = str(0)
            result['month_history'] = str(0)
            result['week_history'] = str(0)
            result['day_history'] = str(0)
        else:
            result['year_history'] = day_trdDd_matching(
                cal_year_history(api.get_stock_history(marketcode, issuecode,
                                                                    'M', '19800101', datetime.today().strftime('%Y%m%d'), 50)))
            if result['year_history'] is False:
                    result['year_history'] = str(0)

            result['month_history'] = day_trdDd_matching(
                api.get_stock_history(marketcode, issuecode,
                                            'M', '19800101', datetime.today().strftime('%Y%m%d'), 50))
            if result['month_history'] is False:
                result['month_history'] = str(0)
            result['week_history'] = day_trdDd_matching(
                api.get_stock_history(marketcode, issuecode,
                                            'W', '19800101', datetime.today().strftime('%Y%m%d'), 50))

            if result['week_history'] is False:
                result['week_history'] = str(0)

            result['day_history'] = day_trdDd_matching(
                api.get_stock_history(marketcode, issuecode,
                                            'D', '19800101', datetime.today().strftime('%Y%m%d'), 50))
            if result['day_history'] is False:
                result['day_history'] = str(0)
    else:
        if marketcode == 'nasdaq':
            return redirect('/nasdaq_stock_info' + '/' + marketcode + '/' + issuecode)
        else:
            return redirect('/stock_info' + '/' + marketcode + '/' + issuecode)

    if marketcode == 'nasdaq':
        return render(request, 'nasdaq_stock_info.html', {'result': result, 'star':star})
    else:
        return render(request, 'stock_info.html', {'result': result, 'star':star})


def cal_year_history(history):
    try:
        temp_year = ''
        year_trdPrc = []
        for element in history:
            cur_year = str(element['trdDd'])[0:4]
            if cur_year != temp_year:
                temp_year = cur_year
                year_trdPrc.append(element)
        return year_trdPrc
    except Exception as e:
        print('Error in cal_year_history: \n', e)
        return False


def boomark(request, marketcode, isuSrtCd ):
    if request.method == 'POST':
        mark = bookmark.objects.filter(user_id =request.user.user_id, marketcode = marketcode, isuSrtCd = isuSrtCd)
        if mark :
            mark.delete()
        else:
            bookmark.objects.create(
                user_id =request.user.user_id,
                marketcode = marketcode,
                isuSrtCd = isuSrtCd,
                activate = 1
            )
        data = json.loads(request.body)
        context = {
            'result': data,
        }
        return JsonResponse(context)


def day_trdDd_matching(history):
    day_trdDd_array = []
    try:
        for element in history:
            day_trdDd_array.append({'trdDd': element['trdDd'], 'trdPrc': element['trdPrc']})
        return list(reversed(day_trdDd_array))
    except Exception as e:
        print('Error in day_trdDd_matching: \n', e)
        return False


def current_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        result = kocom.api().get_current_stock(data['marketcode'], data['issuecode'])
    return JsonResponse({'result': result}, content_type='application/json')


def stock_search_result(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        try:
            totalmerge = Totalmerge.objects.filter(name__icontains=data)
            result = []
            for elements in totalmerge:
                result.append({
                    'logo': elements.logo,
                    'isukorabbrv': elements.name,
                    'issuecode': elements.id,
                    'marketcode': elements.marketcode
                })
        except Exception as e:
            print('Error in stock_search_result: \n', e)
    return JsonResponse({'result': result}, content_type='application/json')


def buy_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        total_rest_investment = cal.calculator().total_use_investment_amount(request.user.user_id)
        buy_price = int(data['share']) * int(data['current_price'])
        if (request.user.invest + total_rest_investment) - buy_price < 0:
            return JsonResponse({'result': '가상잔액이 부족합니다'}, content_type='application/json')
        try:
            stock_master = kocom.api().get_stock_master(data['marketcode'], data['issuecode'])
            stockheld_check = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                       sh_isusrtcd=stock_master['isuSrtCd']).exists()
            with transaction.atomic():
                if stock_master and not stockheld_check:
                    stockheld_insert(request.user.user_id, data, stock_master)
                    stocktrading_insert(request.user.user_id, data, stock_master, 'B')
                    stockprofit_input(request.user.user_id, data, 'B')
                elif stock_master and stockheld_check:
                    stockheld_update(request.user.user_id, data, stock_master, 'B')
                    stocktrading_insert(request.user.user_id, data, stock_master, 'B')
                    stockprofit_input(request.user.user_id, data, 'B')
                result = True
        except Exception as e:
            print('Error in buy_stock: \n', e)
            result = False
    return JsonResponse({'result': result}, content_type='application/json')


def sold_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        get_share = cal.calculator().get_shares(request.user.user_id, data['issuecode'])
        sold_share = int(data['share'])
        if get_share - sold_share < 0:
            return JsonResponse({'result': '보유 주가 부족합니다'}, content_type='application/json')
        elif get_share - sold_share == 0:
            data['sh_z_date'] = datetime.now()

        try:
            stock_master = kocom.api().get_stock_master(data['marketcode'], data['issuecode'])
            stockheld_check = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                       sh_isusrtcd=stock_master['isuSrtCd']).exists()
            with transaction.atomic():
                if stock_master and stockheld_check:
                    stockheld_update(request.user.user_id, data, stock_master, 'S')
                    stocktrading_insert(request.user.user_id, data, stock_master, 'S')
                    stockprofit_input(request.user.user_id, data, 'S')
                result = True
        except Exception as e:
            print('Error in sold_stock: \n', e)
            result = False
    return JsonResponse({'result': result}, content_type='application/json')


def stockheld_insert(user_id, data, master):
    Stockheld(
        sh_userid=acc_models.user.objects.get(user_id=user_id),
        sh_isusrtcd=master['isuSrtCd'],
        sh_isucd=master['isuCd'],
        sh_isukorabbrv=master['isuKorAbbrv'],
        sh_marketcode=data['marketcode'],
        sh_idxindmidclsscd=master['idxIndMidclssCd'],
        sh_share=data['share'],
        sh_price=-(int(data['share']) * int(data['current_price'])),
        sh_z_date=datetime(1, 1, 1, 1, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    ).save()


def stockheld_update(user_id, data, master, kind):
    share = int(data['share'])
    price = int(data['share']) * int(data['current_price'])
    if kind == 'B':
        price = -price
    if kind == 'S':
        share = -share
    stockheld_objects = Stockheld.objects.get(sh_userid=acc_models.user.objects.get(user_id=user_id),
                                              sh_isusrtcd=master['isuSrtCd'])
    stockheld_objects.sh_share += share
    stockheld_objects.sh_price += price
    if 'sh_z_date' in data:
        stockheld_objects.sh_z_date = data['sh_z_date']
    stockheld_objects.save()


def stocktrading_insert(user_id, data, master, kind):
    price = int(data['current_price'])
    if kind == 'B':
        price = -price
    print(f'stocktrading Insert: {user_id}, {price}')
    Stocktrading(
        st_userid=acc_models.user.objects.get(user_id=user_id),
        st_isusrtcd=master['isuSrtCd'],
        st_kind=kind,
        st_share=data['share'],
        st_price=price
    ).save()


def stockprofit_input(user_id, data, kind):
    price = int(data['share']) * int(data['current_price'])
    if kind == 'B':
        price = -price
    stockprofit_check = Stockprofit.objects.filter(sp_userid=user_id).exists()
    if not stockprofit_check:
        print(f'stockprofit Insert: {user_id}, {price}')
        Stockprofit(
            sp_userid=acc_models.user.objects.get(user_id=user_id),
            sp_profit=price,
        ).save()
    else:
        print(f'stockprofit Update: {user_id}, {price}')
        stockprofit_objects = Stockprofit.objects.get(sp_userid=user_id)
        stockprofit_objects.sp_userid = acc_models.user.objects.get(user_id=user_id)
        stockprofit_objects.sp_profit += price
        stockprofit_objects.save()


def get_selectivemaster(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        result = kocom.api().get_selectivemaster(data['marketcode'], data['issuecode'])
    return JsonResponse({'result': result}, content_type='application/json')


def stocksector_update(request):
    if request.method == 'POST':
        # stocksectors_bundle = kocom.api().get_stocksectors_bundle()
        stocksectors_bundle = iex.api().get_stocksectors_bundle()
        if stocksectors_bundle:
            stocksector_insert(stocksectors_bundle)
            return JsonResponse({'result': 'Success'}, content_type='application/json')
        else:
            return JsonResponse({'result': 'Fail'}, content_type='application/json')


def stocksector_insert(stocksectors_bundle):
    print('==================> Start insert StockSector <==================')
    for stocksector in stocksectors_bundle:
        stocksector_check = Stocksector.objects.filter(ss_isusrtcd=stocksector['isusrtcd']).exists()
        if not stocksector_check:
            print('Insert: ', stocksector['isusrtcd'])
            Stocksector(
                ss_isusrtcd=stocksector['isusrtcd'],
                ss_isukorabbrv=stocksector['isukorabbrv'],
                ss_marketcode=stocksector['marketcode'],
                ss_idxindmidclsscd=stocksector['idxindmidclsscd'],
                ss_haltyn=stocksector['haltyn'],
            ).save()
        else:
            print('Update: ', stocksector['isusrtcd'])
            stocksector_objects = Stocksector.objects.get(ss_isusrtcd=stocksector['isusrtcd'])
            stocksector_objects.ss_isukorabbrv = stocksector['isukorabbrv']
            stocksector_objects.ss_marketcode = stocksector['marketcode']
            stocksector_objects.ss_idxindmidclsscd = stocksector['idxindmidclsscd']
            stocksector_objects.ss_haltyn = stocksector['haltyn']
            stocksector_objects.save()


def get_history(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        result = kocom.api().get_stock_history(data['marketcode'], data['issuecode'],
                                               data['trnsmCycleTpCd'], data['inqStrtDd'],
                                               data['inqEndDd'], data['reqCnt'])
    return JsonResponse({'result': result}, content_type='application/json')


def per_pbr_update(request):
    result = False
    if request.method == 'POST':
        data = json.loads(request.body) # 여기서부터 코스피 perpbr 버튼 , 나스닥 perpbr 버튼 구분
        print(data) # 여기서 portfolio.html 의 perpbr button 태그 내 value 가 출력됩니다. (kospi or nasdaq)
        ############

        koscom_api = kocom.api()
        try:
            per_pbr_bundle = koscom_api.get_per_pbr_bundle()
            if per_pbr_bundle:
                per_pbr_insert(per_pbr_bundle)
                result = True
        except Exception as e:
            print('Error in per_pbr_update: \n', e)
        return JsonResponse({'result': result}, content_type='application/json')


def per_pbr_insert(per_pbr_bundle):
    print('==================> Start insert per_pbr <==================')
    not_exists_list = []
    for per_pbr in per_pbr_bundle:
        try:
            totalmerge_check = Totalmerge.objects.filter(id=per_pbr['isusrtcd']).exists()
            if totalmerge_check:
                totalmerge_objects = Totalmerge.objects.get(id=per_pbr['isusrtcd'])
                totalmerge_objects.per = per_pbr['per']
                totalmerge_objects.pbr = per_pbr['pbr']
                totalmerge_objects.save()
                print(f'update: {per_pbr["isusrtcd"]}')
        except Exception as e:
            print(f'Error in per_pbr_insert: \n{e}\n !!!!But wait for finish this task!!!!')
            not_exists_list.append(per_pbr['isusrtcd'])
    print('==================> Finish insert per_pbr <==================')
    print(f'not exists list \n {not_exists_list}')
