from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from . import kocom
from . import stockcal as cal
from .models import *
from accounts import models as acc_models


def search_stock(request):
    return render(request, 'search_stock.html')


def stock(request):
    stockheld = Stockheld.objects.filter(sh_userid=request.user.user_id)

    stock_data = []
    stock_cal = cal.calculator()
    koscom_api = kocom.api()
    for element in stockheld:
        average_price = stock_cal.average_price(request.user.user_id, element.sh_isusrtcd)
        current_price = koscom_api.get_current_price(element.sh_marketcode, element.sh_isusrtcd)
        stock_data.append([element.sh_isukorabbrv, average_price, current_price])
    return render(request, 'stock.html', {'stock_data': stock_data})


def portfolio(request):
    # 구매하기가 같은 페이지에 있어서 임시로 넣어둔 값
    # data = {'marketcode': 'kospi', 'issuecode': '035420'}
    data = {}

    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    total_current_price = stock_cal.total_current_price(request.user.user_id)
    if total_current_price == False:
        return render(request, 'portfolio.html')

    if total_investment_amount and total_investment_amount:
        data['total_investment_amount'] = total_investment_amount
        data['total_current_price'] = total_current_price
    return render(request, 'portfolio.html')


def current_stock(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        result = kocom.api().get_current_stock(data['marketcode'], data['issuecode'])
    return JsonResponse({'result': result}, content_type='application/json')


def buy_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        rest_investment = cal.calculator().total_rest_investment_amount(request.user.user_id, data['issuecode'])
        buy_price = int(data['share']) * int(data['current_price'])
        if (request.user.invest - rest_investment) - buy_price < 0:
            return JsonResponse({'result': '가상잔액이 부족합니다'}, content_type='application/json')

        stock_master = kocom.api().get_stock_master(data['marketcode'], data['issuecode'])
        stockheld_check = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                   sh_isusrtcd=stock_master['isuSrtCd']).exists()
        if stock_master and not stockheld_check:
            if stockheld_insert(request.user.user_id, data, stock_master):
                result = stocktrading_insert(request.user.user_id, data, stock_master, 'B')
        elif stock_master and stockheld_check:
            result = stocktrading_insert(request.user.user_id, data, stock_master, 'B')
        elif not stock_master and stockheld_check:
            result = False
        elif not stock_master and not stockheld_check:
            result = False
    return JsonResponse({'result': result}, content_type='application/json')


def sold_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        rest_investment = cal.calculator().total_rest_investment_amount(request.user.user_id, data['issuecode'])
        sold_price = int(data['share']) * int(data['current_price'])
        if rest_investment - sold_price < 0:
            return JsonResponse({'result': '투자잔액이 부족합니다'}, content_type='application/json')

        stock_master = kocom.api().get_stock_master(data['marketcode'], data['issuecode'])
        stockheld_check = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                   sh_isusrtcd=stock_master['isuSrtCd']).exists()
        if stock_master and stockheld_check:
            result = stocktrading_insert(request.user.user_id, data, stock_master, 'S')
    return JsonResponse({'result': result}, content_type='application/json')


def stockheld_insert(user_id, data, master):
    try:
        Stockheld(
            sh_userid=acc_models.user.objects.get(user_id=user_id),
            sh_isusrtcd=master['isuSrtCd'],
            sh_isucd=master['isuCd'],
            sh_isukorabbrv=master['isuKorAbbrv'],
            sh_marketcode=data['marketcode'],
            sh_idxindmidclsscd=master['idxIndMidclssCd']
        ).save()
        return True
    except Exception as e:
        print('Error in set_stockheld: \n', e)
        return False


def stocktrading_insert(user_id, data, master, kind):
    try:
        if kind == 'S':
            data['current_price'] = -int(data['current_price'])
        Stocktrading(
            st_userid=acc_models.user.objects.get(user_id=user_id),
            st_isusrtcd=master['isuSrtCd'],
            st_kind=kind,
            st_share=data['share'],
            st_price=data['current_price']
        ).save()
        return True
    except Exception as e:
        print('Error in set_stocktrading: \n', e)
        return False


def get_selectivemaster(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        result = kocom.api().get_selectivemaster(data['marketcode'], data['issuecode'])
    return JsonResponse({'result': result}, content_type='application/json')


def stocksector_update(request):
    if request.method == 'POST':
        stocksectors_bundle = kocom.api().get_stocksectors_bundle()
        if stocksectors_bundle:
            stocksector_insert(stocksectors_bundle)
            return JsonResponse({'result': 'Success'}, content_type='application/json')
        else:
            return JsonResponse({'result': 'Fail'}, content_type='application/json')


def stocksector_insert(stocksectors_bundle):
    print('==================> Start insert StockSector <==================')
    for stocksector in stocksectors_bundle:
        stockheld_check = Stocksector.objects.filter(ss_isusrtcd=stocksector['isusrtcd']).exists()
        if not stockheld_check:
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
            stocksector_objects.ss_isusrtcd = stocksector['isusrtcd']
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
