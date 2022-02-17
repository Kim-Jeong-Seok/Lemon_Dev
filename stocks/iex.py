import json
import requests
from mysettings import IEX_C_TOKEN


class api:
    def __init__(self):
        self.timeout = 3

    def get_current_stock(self, symbol):
        try:
            url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={IEX_C_TOKEN}'
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return False
        except Exception as e:
            print('Error in get_current_stock: \n', e)
            return False

    def get_current_price(self, symbol):
        try:
            url = f'https://cloud.iexapis.com/stable/stock/{symbol}/price?token={IEX_C_TOKEN}'
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return False
        except Exception as e:
            print('Error in get_current_price: \n', e)
            return False

    def get_stock_master(self, symbol):
        try:
            url = f'https://cloud.iexapis.com/stable/stock/{symbol}/company?token={IEX_C_TOKEN}'
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return False
        except Exception as e:
            print('Error in get_stock_master: \n', e)
            return False

    def get_selectivemaster(self, symbol):
        try:
            url = f'https://cloud.iexapis.com/stable/time-series/FUNDAMENTAL_VALUATIONS/{symbol}?token={IEX_C_TOKEN}'
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                result = json.loads(response.text)
                return {'symbol': symbol, 'per': round(result[0]['pToE'], 2), 'pbr': round(result[0]['pToBv'], 2)}
            else:
                return False
        except Exception as e:
            print('Error in get_selectivemaster: \n', e)
            return False

    def get_stocksectors_bundle(self):
        result = []
        stocks_list = self.stocks_list()
        if stocks_list:
            for stock in stocks_list:
                get_stocksector = self.get_stocksector(stock['symbol'])
                if get_stocksector:
                    print(stock)
                    result.append({
                        'isusrtcd': stock['symbol'],
                        'isukorabbrv': stock['name'],
                        'marketcode': 'nasdaq',
                        'idxindmidclsscd': get_stocksector['sector'],
                        'haltyn': 'N'
                    })
                else:
                    print('========>Fail get stocksector: ', stock['symbol'])
        else:
            return False
        return result

    def stocks_list(self):
        try:
            url = f'https://cloud.iexapis.com/beta/ref-data/symbols?token={IEX_C_TOKEN}'
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return
        except Exception as e:
            print('Error in stocks_list: \n', e)
            return False

    def get_stocksector(self, symbol):
        try:
            url = f'https://cloud.iexapis.com/stable/tops?symbols={symbol}&token={IEX_C_TOKEN}'
            response = requests.get(url, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)[0]
            else:
                return False
        except Exception as e:
            print('Error in get_stocksector: \n', e)
            return False



    def get_per_pbr_bundle(self):
        result = []
        stocks_list = self.stocks_list()
        if stocks_list:
            for stock in stocks_list:
                get_stocksector = self.get_selectivemaster(stock['symbol'])
                if get_stocksector:
                    print(get_stocksector)
                    result.append({
                        'isusrtcd': get_stocksector['symbol'],
                        'per': get_stocksector['per'],
                        'pbr': get_stocksector['pbr'],
                    })
                else:
                    print('========>Fail get stocksector: ', stock['symbol'])
        else:
            return False
        return result
