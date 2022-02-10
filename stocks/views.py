from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from . import kocom
from . import stockcal as cal
from .models import *
from accounts import models as acc_models
from stocks.models import Stocksector


def search_stock(request):
    wntlr = Totalmerge.objects.all().values('id', 'name')
    return render(request, 'search_stock.html', {'wntlr': wntlr})


def stock(request):
    stockheld = Stockheld.objects.filter(~Q(sh_share=0), sh_userid=request.user.user_id)

    stock_data = []
    stock_cal = cal.calculator()
    koscom_api = kocom.api()
    for element in stockheld:
        average_price = stock_cal.average_price(request.user.user_id, element.sh_isusrtcd)
        current_price = koscom_api.get_current_price(element.sh_marketcode, element.sh_isusrtcd)
        stock_data.append(
            [element.sh_isukorabbrv, average_price, current_price, element.sh_isusrtcd, element.sh_marketcode])
    return render(request, 'stock.html', {'stock_data': stock_data})


def portfolio(request):
    result = {}
    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    total_current_price = stock_cal.total_current_price(request.user.user_id)
    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
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
                                                                                                      'M', '19800101', datetime.today().strftime('%Y%m%d'), 50)))
            result['month_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                      'M', '19800101', datetime.today().strftime('%Y%m%d'), 50))
            result['week_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                     'W', '19800101', datetime.today().strftime('%Y%m%d'), 50))
            result['day_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                    'D', '19800101', datetime.today().strftime('%Y%m%d'), 50))
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
                elif stock_master and stockheld_check:
                    stockheld_update(request.user.user_id, data, stock_master, 'B')
                    stocktrading_insert(request.user.user_id, data, stock_master, 'B')
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
    if kind == 'B':
        data['current_price'] = -int(data['current_price'])
    Stocktrading(
        st_userid=acc_models.user.objects.get(user_id=user_id),
        st_isusrtcd=master['isuSrtCd'],
        st_kind=kind,
        st_share=data['share'],
        st_price=data['current_price']
    ).save()


def stock_profit_input(user_id, price):
    stockprofit_check = Stockprofit.objects.filter(sp_userid=user_id).exists()
    if not stockprofit_check:
        print(f'Insert: {user_id}, {price}')
        Stockprofit(
            sp_userid=user_id,
            sp_profit=price,
        ).save()
    else:
        print(f'Update: {user_id}, {price}')
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
        stocksectors_bundle = kocom.api().get_stocksectors_bundle()
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


def per_pbr_update(request):
    result = False
    if request.method == 'POST':
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
    print(print('==================> Finish insert per_pbr <=================='))
    print(f'not exists list \n {not_exists_list}')
