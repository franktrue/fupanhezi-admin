from stock.utils.date import last_day_of_last_quarter
from django.core.cache import cache
import akshare as ak

class StockInfoService():

    def __init__(self) -> None:
        self.timeout = 24*3600

    # 个股信息
    def info(self, symbol):
        key = "stock_info:{0}".format(symbol)
        data = cache.get(key)
        if data is None:
            df = ak.stock_individual_info_em(symbol=symbol)
            data = df.set_index('item')['value'].to_dict()
            cache.set(key, data, timeout=self.timeout)
        return data
    
    # 主营介绍
    def zyjs(self, symbol):
        key = "stock_zyjs:{0}".format(symbol)
        data = cache.get(key)
        if data is None:
            df = ak.stock_zyjs_ths(symbol=symbol)
            data = df.to_dict("records")[0]
            cache.set(key, data, timeout=self.timeout)
        return data
    
    # 十大股东
    def gdfx_top(self, symbol):
        key = "stock_gdfx_top:{0}".format(symbol)
        data = cache.get(key)
        if data is None:
            # 判断是上证还是深证
            if  symbol[0] == '6':
                full_stock_code = 'sh' + symbol
            else:
                full_stock_code = 'sz' + symbol
            date = last_day_of_last_quarter()
            df = ak.stock_gdfx_top_10_em(symbol=full_stock_code, date=date.strftime("%Y%m%d"))
            df = df.fillna(0)
            data = df.to_dict("records")
            cache.set(key, data, timeout=self.timeout)
        return data

    # 十大流通股东
    def gdfx_free_top(self, symbol):
        key = "stock_gdfx_free_top:{0}".format(symbol)
        data = cache.get(key)
        if data is None:
            # 判断是上证还是深证
            if  symbol[0] == '6':
                full_stock_code = 'sh' + symbol
            else:
                full_stock_code = 'sz' + symbol
            date = last_day_of_last_quarter()
            df = ak.stock_gdfx_free_top_10_em(symbol=full_stock_code, date=date.strftime("%Y%m%d"))
            df = df.fillna(0)
            data = df.to_dict("records")
            cache.set(key, data, timeout=self.timeout)
        return data
    
    # 个股新闻
    def news(self, symbol):
        key = "stock_news:{0}".format(symbol)
        data = cache.get(key)
        if data is None:
            df = ak.stock_news_em(symbol=symbol).head(10)
            data = df.to_dict("records")
            # 新闻缓存1h即可
            cache.set(key, data, timeout=3600)
        return data