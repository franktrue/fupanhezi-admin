from stock.models import StockBoardConcept, StockBoardIndustry, StockBoardMap, StockBoardHistory
from stock.utils.db import get_engine
from django.db import connections
from stock.utils.date import is_trade_date
import datetime
import akshare as ak
import pywencai

class StockBoardService():
    def __init__(self):
        self.engine = get_engine()

    # 更新概念
    def fetch_concept(self):
        df = ak.stock_board_concept_name_ths()
        df.columns = ['release_date', 'name', 'include_number', 'show_url', 'code']
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(StockBoardConcept._meta.db_table))
        df.to_sql(name=StockBoardConcept._meta.db_table, con=self.engine, if_exists="append", index=False)

    # 更新行业
    def fetch_industry(self):
        df = ak.stock_board_industry_name_ths()
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(StockBoardIndustry._meta.db_table))
        df.to_sql(name=StockBoardIndustry._meta.db_table, con=self.engine, if_exists="append", index=False)
    
    # 更新成分股
    def update_cons(self, symbol, name, type):
        print(symbol, name, type)
        df = ak.stock_board_cons_ths(symbol=symbol)
        df = df[['代码', '名称']]
        df.columns = ['stock_code', 'stock_name']
        df['code'] = symbol
        df['board_name'] = name
        df['type'] = type
        # 先删除旧数据
        StockBoardMap.objects.filter(code=symbol).delete()
        df.to_sql('stock_board_map', con=self.engine, if_exists="append", index=False)

    # 更新板块行情
    def fetch_history(self, trade_date):
        trade_date_str = trade_date.strftime("%Y%m%d")
        df=pywencai.get(question="同花顺概念指数{0}开盘价 {0}最高价 {0}最低价 {0}收盘价 {0}涨跌幅".format(trade_date_str), query_type="zhishu", loop=True)
        col_zh = [
            "code", 
            "指数简称", 
            "指数@开盘价:不复权[{0}]".format(trade_date_str), 
            "指数@最高价:不复权[{0}]".format(trade_date_str), 
            "指数@最低价:不复权[{0}]".format(trade_date_str), 
            "指数@收盘价:不复权[{0}]".format(trade_date_str), 
            "指数@涨跌幅:前复权[{0}]".format(trade_date_str), 
            "指数@成交额[{0}]".format(trade_date_str), 
            "指数@成交量[{0}]".format(trade_date_str),
            "指数@换手率[{0}]".format(trade_date_str)
        ]
        df = df[col_zh]
        df.columns = ['code', 'name', 'open', 'high', 'low', 'close', 'close_pe', 'vol', 'amo', 'hs_rate']
        df = df[~df['open'].isna()]
        df['date'] = trade_date
        StockBoardHistory.objects.filter(date=trade_date).delete()
        df.to_sql(name=StockBoardHistory._meta.db_table, con=self.engine, if_exists="append", index=False)

    def fetch_history_by_task(self, trade_date):
        trade_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d').date()
        self.fetch_history(trade_date=trade_date)
