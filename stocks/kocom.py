import json
import requests
from mysettings import KOSCOM_KEY


class api:
    def __init__(self):
        self.timeout = 3

    def get_current_stock(self, marketcode, issuecode):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/{issuecode}/price'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']
            else:
                return False
        except Exception as e:
            print('Error in get_current_stock: \n', e)
            return False



    def get_current_price(self, marketcode, issuecode):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/{issuecode}/price'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']['trdPrc']
            else:
                return False
        except Exception as e:
            print('Error in get_current_price: \n', e)
            return False

    def test_get_current_price(self, stock):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/kospi/{stock}/price'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']['trdPrc']
            else:
                url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/kosdaq/{stock}/price'
                headers = {'apikey': KOSCOM_KEY}
                response = requests.get(url, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    return json.loads(response.text)['result']['trdPrc']
                else:
                    return False
        except Exception as e:
            print('Error in get_current_price: \n', e)
            return False


    def get_stock_master(self, marketcode, issuecode):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/{issuecode}/master'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']
            else:
                return False
        except Exception as e:
            print('Error in get_stock_master: \n', e)
            return False

    def get_selectivemaster(self, marketcode, issuecode):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/{issuecode}/selectivemaster?per&pbr'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']
            else:
                return False
        except Exception as e:
            print('Error in get_selectivemaster: \n', e)
            return False

    def get_stocksectors_bundle(self):
        result = []
        marketcode = ['kospi', 'kosdaq']
        for code in marketcode:
            list = self.stocks_list(code)
            if list:
                for stock in list:
                    get_stocksector = self.get_stocksector(code, stock['isuSrtCd'])
                    if get_stocksector:
                        print(stock)
                        print(get_stocksector['isuKorAbbrv'])
                        result.append({
                            'isusrtcd': get_stocksector['isuSrtCd'],
                            'isukorabbrv': get_stocksector['isuKorAbbrv'],
                            'marketcode': code,
                            'idxindmidclsscd': get_stocksector['idxIndMidclssCd'],
                            'haltyn': get_stocksector['haltYn']
                        })
                    else:
                        print('========>Fail get stocksector: ', stock['isuSrtCd'])
            else:
                return False
        return result

    def stocks_list(self, marketcode):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/lists'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['isuLists']
            else:
                return
        except Exception as e:
            print('Error in stocks_list: \n', e)
            return False

    def get_stocksector(self, marketcode, issucode):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/{issucode}/master'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']
            else:
                return False
        except Exception as e:
            print('Error in get_stocksector: \n', e)
            return False

    def get_stock_history(self, marketcode, issuecode, trnsmCycleTpCd, inqStrtDd, inqEndDd, reqCnt):
        try:
            url = f'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/{marketcode}/{issuecode}/history' \
                  f'?trnsmCycleTpCd={trnsmCycleTpCd}&inqStrtDd={inqStrtDd}&inqEndDd={inqEndDd}&reqCnt={reqCnt}'
            headers = {'apikey': KOSCOM_KEY}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return json.loads(response.text)['result']['hisLists']
            else:
                return False
        except Exception as e:
            print('Error in get_stock_history: \n', e)
            return False
