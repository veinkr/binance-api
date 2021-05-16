# -*- coding:utf-8 -*-
"""
filename : example.py
createtime : 2021/5/16 15:40
author : Demon Finch
"""
import os

from binance_api_setting import api_key, api_secret
from binance_api import *

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
if __name__ == '__main__':
    print(f"localtime start:{datetime.now()}")

    print("binance合约验证")
    binance_f = Binanceapi(api_keys=api_key, secret_key=api_secret, host='https://fapi.binance.com')
    ret = binance_f.get_data(api="/fapi/v1/continuousKlines",
                             method=RequestMethod.GET,
                             sign=False,
                             pair='ETHUSDT',
                             contractType='PERPETUAL',
                             interval='1m')
    print(ret.status_code)
    print(ret.text[:50])

    ret = binance_f.get_data(api="/fapi/v2/account",
                             method=RequestMethod.GET,
                             sign=True
                             )
    print(ret.status_code)
    print(ret.text[:50])

    print("现货接口验证")
    binance_d = Binanceapi(api_keys=api_key, secret_key=api_secret, host='https://api.binance.com')
    ret = binance_d.get_data(api="/sapi/v1/mining/pub/coinList",
                             method=RequestMethod.GET,
                             sign=True
                             )
    print(ret.status_code)
    print(ret.text)

    ret = binance_d.get_data(api="/api/v3/ping",
                             method=RequestMethod.GET,
                             sign=False,
                             notime=True
                             )
    print(ret.status_code)
    print(ret.text)

    print(f"localtime end:{datetime.now()}")
