from stock.models import StockTradeDate
from stock.utils.db import get_engine
from django.db import connections
from stock.utils.cache import delete_cache_by_prefix
import akshare as ak
import datetime

class StockTradeDateService():
    def __init__(self):
        self.engine = get_engine()
        self.table_name = StockTradeDate._meta.db_table
    
    def fetch(self):
        trade_date = ak.tool_trade_date_hist_sina()
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(self.table_name))
        trade_date.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)

    # 清空前端缓存（最近的20个工作日）
    def clearCache(self):
        today = datetime.date.today()
        # 获取20天交易日
        trade_date_range = StockTradeDate.objects.filter(trade_date__lte=today).order_by("-trade_date")[:20]
        prefix = "cache:fupanhezi:stockZtHistory:ztRow_"
        for trade_date in trade_date_range:
            delete_cache_by_prefix(prefix=prefix+trade_date.trade_date.strftime("%Y-%m-%d"))

        # 题材相关API缓存
        delete_cache_by_prefix(prefix="cache:fupanhezi:stockBoardMap:Board:")
