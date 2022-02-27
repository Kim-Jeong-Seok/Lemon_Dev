from .models import *
from . import koscom
from django.db.models import Sum, F


class calculator:
    def __init__(self):
        pass

    # 현재 있는 주식에 대한 전체 구매한 양
    def total_investment_amount(self, user_id):
        total_buy = 0
        try:
            stockheld = Stockheld.objects.filter(sh_userid=user_id).exclude(sh_share__lte=0)
            if stockheld.exists():
                for element in stockheld:
                    stocktrading = Stocktrading.objects.filter(st_userid=user_id,
                                                               st_isusrtcd=element.sh_isusrtcd,
                                                               st_kind='B',
                                                               st_date__gt=element.sh_z_date).aggregate(
                        total=Sum(F('st_price') * F('st_share')))['total']
                    total_buy += stocktrading
                return -total_buy
            else:
                return False
        except Exception as e:
            print('Error in total_buy_investment_amount: \n', e)
            return False

    # 전체 매도금액 (사용안해 update 안함)
    def total_profit_amount(self, user_id):
        try:
            elements_sum = Stocktrading.objects.filter(st_userid=user_id,
                                                       st_kind='S').aggregate(
                                sum=Sum(F('st_price') * F('st_share')))['sum']
            return elements_sum
        except Exception as e:
            print('Error in total_profit_amount: \n', e)
            return False

    # 현재 있는 주식에 대한 전체 현재가
    def total_current_price(self, user_id):
        total_current_price = 0
        try:
            stockheld = Stockheld.objects.filter(sh_userid=user_id).exclude(sh_share__lte=0)
            if stockheld.exists():
                for element in stockheld:
                    current_price = koscom.api().get_current_price(element.sh_marketcode, element.sh_isusrtcd)
                    if current_price:
                        total_current_price += current_price * element.sh_share
                        return total_current_price
                    else:
                        return False
            else:
                return False
        except Exception as e:
            print('Error in total_current_price: \n', e)
            return False

    # 전체 손익금
    def total_profit_n_loss(self, user_id):
        try:
            total_profit_n_loss = 0
            stockheld_list = Stockheld.objects.filter(sh_userid=user_id)
            if stockheld_list[0]:
                for stockheld in stockheld_list:
                    average_price = self.total_history_average_price(user_id, stockheld.sh_isusrtcd)
                    element = Stocktrading.objects.filter(st_userid=user_id,
                                                          st_isusrtcd=stockheld.sh_isusrtcd,
                                                          st_kind='S').aggregate(
                        total=Sum(F('st_price') * F('st_share')), share_total=Sum('st_share'))
                    total = element['total'] or 0
                    share_total = element['share_total'] or 0
                    total_profit_n_loss += (total - average_price * share_total)
            return total_profit_n_loss
        except Exception as e:
            print('Error in total_profit_n_loss: \n', e)
            return False

    # 전체 기록에 대한 개별 평균단가
    def total_history_average_price(self, user_id, isusrtcd):
        try:
            stocktrading = Stocktrading.objects.filter(st_userid=user_id,
                                                       st_isusrtcd=isusrtcd,
                                                       st_kind='B').aggregate(
                total=Sum(F('st_price') * F('st_share')), share_total=Sum('st_share'))
            return int(-stocktrading['total'] / stocktrading['share_total'])
        except Exception as e:
            print('Error in total_history_average_price: \n', e)
            return False

    # 개별 평균단가
    def average_price(self, user_id, isusrtcd):
        try:
            stockheld = Stockheld.objects.get(sh_userid=user_id, sh_isusrtcd=isusrtcd)
            stocktrading = Stocktrading.objects.filter(st_userid=user_id,
                                                       st_isusrtcd=isusrtcd,
                                                       st_kind='B',
                                                       st_date__gt=stockheld.sh_z_date).aggregate(
                total=Sum(F('st_price') * F('st_share')), share_total=Sum('st_share'))
            return int(-stocktrading['total'] / stocktrading['share_total'])
        except Exception as e:
            print('Error in average_price: \n', e)
            return False

    # 전체 사용한 투자 금액
    def total_use_investment_amount(self, user_id):
        try:
            use_total = Stockprofit.objects.get(sp_userid=user_id).sp_profit
            if use_total:
                return use_total
            else:
                return 0
        except Exception as e:
            print('Error in total_use_investment_amount: \n', e)
            return False

    # 개별 사용한 투자 금액
    def use_investment_amount(self, user_id, isusrtcd):
        try:
            use_total = Stockheld.objects.get(sh_userid=user_id,
                                              sh_isusrtcd=isusrtcd).sh_price
            if use_total:
                return use_total
            else:
                return 0
        except Exception as e:
            print('Error in use_investment_amount: \n', e)
            return False

    # 개별 주식 주
    def get_shares(self, user_id, isusrtcd):
        try:
            total_share = Stockheld.objects.get(sh_userid=user_id,
                                                sh_isusrtcd=isusrtcd).sh_share
            if total_share:
                return total_share
            else:
                return 0
        except Exception as e:
            print('Error in get_shares: \n', e)
            return False

    # 주식 수익률
    def stock_yield(self, know_price, compare_price):
        return round((know_price - compare_price) * 100 / compare_price, 2)

        # 보유 하고 있는 주식 들에 대한 이득금 계산 용도 주식 이득금 계산용도 입니다
    def user_total_investment_amount(self, user_id):
        total_buy = 0
        try:
            stockheld = Stockheld.objects.filter(
                sh_userid=user_id).exclude(sh_share__lte=0)
            if stockheld.exists():
                for element in stockheld:
                    stocktrading = Stocktrading.objects.filter(st_userid=user_id,
                                                               st_isusrtcd=element.sh_isusrtcd,
                                                               st_date__gt=element.sh_z_date,
                                                               ).aggregate(
                        total=Sum(F('st_price') * F('st_share')))['total']
                    total_buy += stocktrading
                return -total_buy
            else:
                return False
        except Exception as e:
            print('Error in total_buy_investment_amount: \n', e)
            return False

    def S_total_investment(self, user_id):
        total_buy = 0
        try:
            stockheld = Stockheld.objects.filter(
                sh_userid=user_id).exclude(sh_share__lte=0)
            if stockheld.exists():
                for element in stockheld:
                    stocktrading1 = Stocktrading.objects.filter(st_userid=user_id,
                                                               st_isusrtcd=element.sh_isusrtcd,
                                                               st_date__gt=element.sh_z_date,
                                                               st_kind__in=['B','S']).exclude(st_kind='B').aggregate(
                        total=Sum(('st_price') ))['total']


                    print(stocktrading1)
                    total_buy += stocktrading1

                return total_buy
            else:
                return False
        except Exception as e:
            print('Error in total_buy_investment_amount: \n', e)
            return False
    def B_total_investment(self, user_id):
        total_buy = 0
        try:
            stockheld = Stockheld.objects.filter(
                sh_userid=user_id).exclude(sh_share__lte=0)
            if stockheld.exists():
                for element in stockheld:
                    stocktrading = Stocktrading.objects.filter(st_userid=user_id,
                                                               st_isusrtcd=element.sh_isusrtcd,
                                                               st_date__gt=element.sh_z_date,
                                                               st_kind__in=['B','S']).exclude(st_kind='S').aggregate(
                        total=Sum(F('st_price') ))['total']

                    print(stocktrading)

                    total_buy += -stocktrading

                return total_buy
            else:
                return False
        except Exception as e:
            print('Error in total_buy_investment_amount: \n', e)
            return False
