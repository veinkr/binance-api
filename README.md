# binance_api

币安api -> 论极简主义与大而全怎么互相拖鞋

## 缘由

binance官方文档网页上的sdk太臃肿复杂，而且难以使用

## 主要参数

##### Binanceapi类

```
api_key：api-key
secret_key：api-secret
host：根据现货或者合约的区别使用不同的host，现货host为https://api.binance.com，合约host为https://fapi.binance.com
```

##### det_data函数

```
api: str  # api的url，如"/api/v3/ping"
method=RequestMethod.GET  # request调用方式，为字符串的GET、POST、DELETE、PUT
sign: bool = False  # 是否需要签名（sha256）
notime: bool = False # 部分api不需要recvWindow和timestamp参数，如"/api/v3/ping"
**kwargs  # 填写api接口的参数，参考example.py
```

## 用法

可直接参考example.py

### 合约

```python
from binance_api import *

binance_f = Binanceapi(api_keys=api_key, secret_key=api_secret, host='https://fapi.binance.com')
ret = binance_f.get_data(api="/fapi/v1/continuousKlines",
                         method=RequestMethod.GET,
                         sign=False,
                         pair='ETHUSDT',
                         contractType='PERPETUAL',
                         interval='1m')
print(ret.status_code)
print(ret.text[:50])
```

### 现货

```python
from binance_api import *

binance_d = Binanceapi(api_keys=api_key, secret_key=api_secret, host='https://api.binance.com')
ret = binance_d.get_data(api="/sapi/v1/mining/pub/coinList",
                         method=RequestMethod.GET,
                         sign=True
                         )
print(ret.status_code)
print(ret.text)
```

