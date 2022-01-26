from .models import *
from . import kocom
from django.db.models import Sum, F


class calculator:
    def __init__(self):
        pass

    # 전체 투자금액
    def total_investment_amount(self, user_id):
        try:
            elements_sum = Stocktrading.objects.filter(st_userid=user_id,
                                                       st_kind='B').aggregate(
                                sum=Sum(F('st_price') * F('st_share')))['sum']
            return elements_sum
        except Exception as e:
            print('Error in total_investment_amount: \n', e)
            return False

    # 전체 현재가
    def total_current_price(self, user_id):
        total_current_price = 1
        try:
            stockheld = Stockheld.objects.filter(sh_userid=user_id)
            
            for elements in stockheld:
                current_price = kocom.api().get_current_price(elements.sh_marketcode, elements.sh_isusrtcd)
                if current_price:
                    total_share = Stocktrading.objects.filter(st_userid=user_id,
                                                              st_isusrtcd=elements.sh_isusrtcd,
                                                              st_kind='B').aggregate(share_total=Sum('st_share'))
                    total_current_price += current_price * total_share['share_total']
                    return total_current_price
                else:
                    return False
        except Exception as e:
            print('Error in total_current_price: \n', e)
            return False

    # 전체 평균단가
    def total_average_price(self, user_id):
        try:
            element = Stocktrading.objects.filter(st_userid=user_id,
                                                  st_kind='B').aggregate(
                total=Sum(F('st_price') * F('st_share')), share_total=Sum('st_share'))
            return round(element['total']/element['share_total'])
        except Exception as e:
            print('Error in total_average_price: \n', e)
            return False

    # 개별 평균단가
    def average_price(self, user_id, isusrtcd):
        try:
            stocktrading = Stocktrading.objects.filter(st_userid=user_id,
                                                       st_isusrtcd=isusrtcd,
                                                       st_kind='B').aggregate(
                total=Sum(F('st_price') * F('st_share')), share_total=Sum('st_share'))
            return round(stocktrading['total'] / stocktrading['share_total'])
        except Exception as e:
            print('Error in average_price: \n', e)
            return False

    # 개별 남은 투자 금액
    def total_rest_investment_amount(self, user_id, isusrtcd):
        try:
            rest_total = Stocktrading.objects.filter(st_userid=user_id,
                                                     st_isusrtcd=isusrtcd).aggregate(
                rest_total=Sum(F('st_price') * F('st_share')))['rest_total']
            return rest_total
        except Exception as e:
            print('Error in total_rest_investment_amount: \n', e)
            return False

    # 주식 수익률
    def stock_yield(self, know_price, compare_price):
        return round((know_price - compare_price) / compare_price, 2)
