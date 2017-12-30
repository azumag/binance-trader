import time
import hashlib
import requests

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

#from urllib.parse import urlencode
#from urllib import urlencode
#https://github.com/purboox/BinanceAPI

class BitflyerAPI:
    BASE_URL = "https://api.bitflyer.jp/v1/"
    BASE_URL_V = "https://api.bitflyer.jp/v1/"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret


    def get_ticker(self, market):
        path = "%s/ticker" % self.BASE_URL
        params = {"product_code": market}
        return self._get_no_sign(path, params)


    def get_orderbooks(self, market, limit=50):
        path = "%s/executions" % self.BASE_URL
        params = {"product_code": market, "count": limit}
        return self._get_no_sign(path, params)


    # def get_account(self):
    #     path = "%s/account" % self.BASE_URL
    #     return self._get(path, {})


    def get_open_orders(self, market, limit = 100):
        path = "%s/getchildorders" % self.BASE_URL
        params = {"product_code": market}
        return self._get(path, params)


    def buy_limit(self, market, quantity, rate):
        path = "%s/sendchildorder" % self.BASE_URL
        params = {"product_code": market, "side": "BUY", \
            "child_order_type": "LIMIT", "time_in_force": "GTC", \
            "size": '%.8f' % quantity, "price": '%.8f' % rate}
        return self._post(path, params)


    def sell_limit(self, market, quantity, rate):
        path = "%s/sendchildorder" % self.BASE_URL
        params = {"product_code": market, "side": "SELL", \
            "child_order_type": "LIMIT", "time_in_force": "GTC", \
            "size": '%.8f' % quantity, "price": '%.8f' % rate}
        return self._post(path, params)


    def buy_market(self, market, quantity):
        path = "%s/sendchildorder" % self.BASE_URL
        params = {"product_code": market, "side": "BUY", \
            "child_order_type": "MARKET", "size": '%.8f' % quantity}
        return self._post(path, params)


    def sell_market(self, market, quantity):
        path = "%s/sendchildorder" % self.BASE_URL
        params = {"product_code": market, "side": "SELL", \
            "child_order_type": "MARKET", "size": '%.8f' % quantity}
        return self._post(path, params)


    def query_order(self, market, orderId):
        path = "%s/getparentorders" % self.BASE_URL
        params = {"product_code": market, "child_order_id": orderId}
        return self._get(path, params)


    def cancel(self, market, order_id):
        path = "%s/cancelchildorder" % self.BASE_URL
        params = {"product_code": market, "child_order_id": order_id}
        return self._delete(path, params)


    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        return requests.get(url, timeout=30, verify=True).json()

# TODO; wip ここまで
    def _sign(self, params={}):
        data = params.copy()

        ts = str(int(1000 * time.time()))
        data.update({"timestamp": ts})

        h = self.secret + "|" + urlencode(data)
        signature = hashlib.sha256(h).hexdigest()
        data.update({"signature": signature})
        return data


    def _get(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, \
            timeout=30, verify=True).json()


    def _post(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.post(url, headers=header, \
            timeout=30, verify=True).json()


    def _delete(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.delete(url, headers=header, \
            timeout=30, verify=True).json()
