from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from datetime import datetime
from . import kocom
from . import stockcal as cal
from .models import *
from accounts import models as acc_models
from stocks.models import Stocksector


def search_stock(request):
    wntlr = Stocksector.objects.all().values('ss_isusrtcd', 'ss_isukorabbrv')
    return render(request, 'search_stock.html', {'wntlr': wntlr})


def stock(request):
    stockheld = Stockheld.objects.filter(sh_userid=request.user.user_id)

    stock_data = []
    stock_cal = cal.calculator()
    koscom_api = kocom.api()
    for element in stockheld:
        average_price = stock_cal.average_price(request.user.user_id, element.sh_isusrtcd)
        current_price = koscom_api.get_current_price(element.sh_marketcode, element.sh_isusrtcd)
        stock_data.append(
            [element.sh_isukorabbrv, average_price, current_price, element.sh_isusrtcd, element.sh_marketcode])
        print(stock_data)
    return render(request, 'stock.html', {'stock_data': stock_data})


def portfolio(request):
    result = {}
    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)

    total_current_price = stock_cal.total_current_price(request.user.user_id)
    print(total_current_price)
    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
    print(total_use_investment_amount)
    if total_investment_amount is False or total_current_price is False or total_use_investment_amount is False:
        result['total_investment_amount'] = 0
        result['total_current_price'] = 0
        result['total_use_investment_amount'] = 0
    else:
        result['total_investment_amount'] = total_investment_amount
        result['total_current_price'] = total_current_price
        result['total_use_investment_amount'] = total_use_investment_amount
    return render(request, 'portfolio.html', result)


def stock_info(request):
    result = False
    koscom_api = kocom.api()
    stock_cal = cal.calculator()
    if request.method == 'POST':
        result = koscom_api.get_stock_master(request.POST['marketcode'], request.POST['issuecode'])
        if result:
            result['curPrice'] = koscom_api.get_current_price(request.POST['marketcode'], request.POST['issuecode'])
            result['marketcode'] = request.POST['marketcode']
            result['total_allow_invest'] = request.user.invest - stock_cal.total_use_investment_amount(request.user.user_id)

            result['year_history'] = day_trdDd_matching(cal_year_history(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                                      'M', '19800101', datetime.today().strftime('%Y%m%d'), 500)))

            result['month_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                      'M', '19800101', datetime.today().strftime('%Y%m%d'), 500))
            result['week_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                     'W', '19800101', datetime.today().strftime('%Y%m%d'), 500))
            result['day_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                    'D', '19800101', datetime.today().strftime('%Y%m%d'), 500))
    return render(request, 'stock_info.html', {'result': result})


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
            stocksector = Stocksector.objects.filter(ss_isukorabbrv__icontains=data)
            result = []
            for elements in stocksector:
                result.append({
                    'logo': elements.ss_logo,
                    'isukorabbrv': elements.ss_isukorabbrv,
                    'issuecode': elements.ss_isusrtcd,
                    'marketcode': elements.ss_marketcode
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
        get_share = cal.calculator().get_shares(request.user.user_id, data['issuecode'])
        sold_share = int(data['share'])
        if get_share - sold_share < 0:
            return JsonResponse({'result': '보유 주가 부족합니다'}, content_type='application/json')

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
        print('Error in stockheld_insert: \n', e)
        return False


def stocktrading_insert(user_id, data, master, kind):
    try:
        if kind == 'B':
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
        print('Error in stocktrading_insert: \n', e)
        return False


def get_selectivemaster(request):
    data = json.loads(request.body)
    result = False
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
