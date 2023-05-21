from stock.models import StockTradeDate
from stock.utils.db import get_engine
from django.db import connections
import akshare as ak

class StockTradeDateService():
    def __init__(self):
        self.engine = get_engine()
        self.table_name = StockTradeDate._meta.db_table
    
    def fetch(self):
        trade_date = ak.tool_trade_date_hist_sina()
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(self.table_name))
        trade_date.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)