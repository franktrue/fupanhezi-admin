from stock.models import StockBoardConcept, StockBoardIndustry, StockBoardMap
from stock.utils.db import get_engine
from django.db import connections
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
