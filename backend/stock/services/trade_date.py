from stock.models import StockTradeDate, StockBoardHistory
from django.db.models import Max
from stock.utils.db import get_engine
from django.db import connections
from stock.utils.cache import delete_cache_by_match
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
            r = trade_date.trade_date.strftime("%Y-%m-%d") + "*"
            delete_cache_by_match(regex=prefix + r)

        # 题材相关API缓存
        delete_cache_by_match(regex="cache:fupanhezi:stockBoardMap:Board:*")

    def clear_cache_by(self, prefix):
        delete_cache_by_match(regex=prefix+"*")

    def clear_board_sort_cache(self):
        latest_date = StockBoardHistory.objects.aggregate(date=Max('date'))['date']
        r1 = "cache:fupanhezi:stockBoardMap:boardCubes_*{0}*".format(latest_date)
        delete_cache_by_match(regex=r1)
        r2 = "cache:fupanhezi:stockBoardMap:Board:ztlb_{0}_*".format(latest_date)
        delete_cache_by_match(regex=r2)
        r3 = "cache:fupanhezi:stockBoardMap:col_{0}:sort:*".format(latest_date)
        delete_cache_by_match(regex=r3)
