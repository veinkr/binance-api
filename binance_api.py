# -*- coding:utf-8 -*-
"""
filename : binance_api.py
createtime : 2021/5/14 16:57
author : Demon Finch
"""
import json
import hashlib
import hmac
from datetime import datetime
from urllib.parse import urlencode
import requests


class RestApiRequest(object):
    def __init__(self, url, method, sign, notime: bool = False):
        self.url = url
        self.method = method
        self.host = None
        self.sign = sign
        self.notime = notime
        self.post_body = ""
        self.header = {"client_SDK_Version": "binance_api_0.0.1"}
        self.param_map = dict()
        self.post_map = dict()

    def put_url(self, name, value):
        if value is not None:
            if isinstance(value, list):
                self.param_map[name] = json.dumps(value)
            elif isinstance(value, float):
                self.param_map[name] = ('%.20f' % value)[slice(0, 16)].rstrip('0').rstrip('.')
            else:
                self.param_map[name] = str(value)

    def build_url(self):
        if len(self.param_map) == 0:
            return ""
        encoded_param = urlencode(self.param_map)
        return encoded_param

    def build_url_to_json(self):
        return json.dumps(self.param_map)


def check_should_not_none(value, name):
    if value is None:
        raise Exception("[Input] " + name + " should not be null")


class CandlestickInterval:
    MIN1 = "1m"
    MIN3 = "3m"
    MIN5 = "5m"
    MIN15 = "15m"
    MIN30 = "30m"
    HOUR1 = "1h"
    HOUR2 = "2h"
    HOUR4 = "4h"
    HOUR6 = "6h"
    HOUR8 = "8h"
    HOUR12 = "12h"
    DAY1 = "1d"
    DAY3 = "3d"
    WEEK1 = "1w"
    MON1 = "1m"
    INVALID = None


class OrderSide:
    BUY = "BUY"
    SELL = "SELL"
    INVALID = None


class TimeInForce:
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"
    INVALID = None


class OrderType:
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_MARKET = "STOP_MARKET"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"
    INVALID = None


class OrderRespType:
    ACK = "ACK"
    RESULT = "RESULT"
    INVALID = None


class MatchRole:
    MAKER = "maker"
    TAKER = "taker"


class DepthStep:
    STEP0 = "step0"
    STEP1 = "step1"
    STEP2 = "step2"
    STEP3 = "step3"
    STEP4 = "step4"
    STEP5 = "step5"


class SubscribeMessageType:
    RESPONSE = "response"
    PAYLOAD = "payload"


class boolean:
    true = 'true'
    flase = 'false'


class TransferType:
    ROLL_IN = "ROLL_IN"
    ROLL_OUT = "ROLL_OUT"
    INVALID = None


class WorkingType:
    MARK_PRICE = "MARK_PRICE"
    CONTRACT_PRICE = "CONTRACT_PRICE"
    INVALID = None


class FuturesMarginType:
    ISOLATED = "ISOLATED"
    CROSSED = "CROSSED"


class PositionSide:
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"
    INVALID = None


class IncomeType:
    TRANSFER = "TRANSFER"
    WELCOME_BONUS = "WELCOME_BONUS"
    REALIZED_PNL = "REALIZED_PNL"
    FUNDING_FEE = "FUNDING_FEE"
    COMMISSION = "COMMISSION"
    INSURANCE_CLEAR = "INSURANCE_CLEAR"
    INVALID = None


class RequestMethod:
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'


class UpdateTime:
    NORMAL = ""
    FAST = "@100ms"
    REALTIME = "@0ms"
    INVALID = ""


class Binanceapi:
    request_method = {"GET": requests.get, "POST": requests.post, "DELETE": requests.delete,
                      "PUT": requests.put}

    def __init__(self, api_keys, secret_key, host: str = None):
        self.api_key = api_keys
        self.secret_key = secret_key
        self.host = host if host else "https://fapi.binance.com"

    def request_combina(self, request: RestApiRequest):
        request.host = self.host
        if request.notime:
            pass
        else:
            request.put_url("recvWindow", 60000)
            request.put_url("timestamp", str(self.timestamp_now))
        if request.sign:
            request.put_url("signature", hmac.new(self.secret_key.encode(),
                                                  msg=request.build_url().encode(),
                                                  digestmod=hashlib.sha256).hexdigest())
            request.header.update({"X-MBX-APIKEY": self.api_key})
        request.header.update({'Content-Type': 'application/json'})
        request.post_body = request.post_map
        request.url = request.url + "?" + request.build_url()
        return request

    def get_data(self, api: str, method=RequestMethod.GET, sign: bool = False, notime: bool = False, **kwargs):
        restapi = RestApiRequest(url=api, method=method, sign=sign, notime=notime)
        print(kwargs)
        for argkey, argvalue in kwargs.items():
            restapi.put_url(argkey, argvalue)
        return self.call_sync(self.request_combina(restapi))

    @property
    def timestamp_now(self):
        return int(round(datetime.now().timestamp() * 1000))

    @staticmethod
    def call_sync(request: RestApiRequest):
        t_start = datetime.now()
        response = Binanceapi.request_method[request.method](request.host + request.url, headers=request.header)
        t_end = datetime.now()
        if response.status_code == 200:
            print(f"接口：{request.method} {request.url.split('?')[0]} -> 耗时：{(t_end - t_start).total_seconds()}s")
            return response
        else:
            print(response.status_code, response.text)
            raise Exception(response.text)


if __name__ == '__main__':
    print(f"localtime start:{datetime.now()}")

    print(f"localtime end:{datetime.now()}")
