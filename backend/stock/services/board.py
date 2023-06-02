from stock.models import StockBoardConcept, StockBoardIndustry, StockBoardMap, StockBoardHistory
from stock.utils.db import get_engine
from django.db import connections
import datetime
import akshare as ak

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
    def fetch_history(self, symbol):
        history = ak.stock_board_concept_hist_ths(start_year="2019", symbol=symbol)
        history.columns = ['date', 'open', 'high', 'low', 'close', 'vol', 'amo']
        history['pre_close'] = history['close'].shift(1)
        history['name'] = symbol
        history['open_pe'] = ((history['open']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history['high_pe'] = ((history['high']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history['low_pe'] = ((history['low']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history['close_pe'] = ((history['close']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history = history[history['date']>=datetime.date(2020, 1, 1)]
        StockBoardHistory.objects.filter(name=symbol).delete()
        history.to_sql(name=StockBoardHistory._meta.db_table, con=self.engine, if_exists="append", index=False)

    def fetch_latest(self, symbol):
        history = ak.stock_board_concept_hist_ths(start_year="2023", symbol=symbol).tail(2)
        history.columns = ['date', 'open', 'high', 'low', 'close', 'vol', 'amo']
        history['pre_close'] = history['close'].shift(1)
        history['name'] = symbol
        history['open_pe'] = ((history['open']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history['high_pe'] = ((history['high']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history['low_pe'] = ((history['low']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        history['close_pe'] = ((history['close']-history['pre_close'])/history['pre_close']*100).apply(lambda x: round(x, 2))
        # 将最后插入数据库一条
        # data = history.to_dict("records")[1]
        history.tail(1).to_sql(name=StockBoardHistory._meta.db_table, con=self.engine, if_exists="append", index=False)
