from stock.models import StockHistory, StockLhb
from stock.utils.db import get_engine
from stock.utils.date import is_trade_date
from django_redis import get_redis_connection
import akshare as ak

class StockLhbService():
    def __init__(self):
        self.engine = get_engine()
        self.table_name = StockLhb._meta.db_table

    def fetch(self, trade_date):
        if is_trade_date(trade_date):
            date_str = trade_date.strftime("%Y%m%d")
            # 龙虎榜详情
            df = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
            df.columns = ["serial", "stock_code", "stock_name", "interpretation", "close", "close_pe", "lhb_net_buy_amo", "lhb_buy_amo", "lhb_sell_amo", "lhb_amo", "market_total_amo", "net_buy_amo_pe", "amo_pe", "hs_rate", "circulate_market_value", "rank_reson"]
            df["date"] = trade_date
            redis_conn = get_redis_connection('default')
            cacheFupanheziStockHistoryIdPrefix = "cache:fupanhezi:stockHistory:id:"
            for row in df.itertuples():
                # 更新数据中的涨停板
                if row.interpretation is None:
                    interpretation = ''
                else:
                    interpretation = row.interpretation
                h = StockHistory.objects.filter(stock_code=row.stock_code, date=trade_date.strftime("%Y-%m-%d")).first()
                if h is not None:
                    h.is_lhb = 1
                    h.lhb_parse = interpretation
                    h.lhb_reson = row.rank_reson
                    h.save()
                    redis_conn.delete("{0}{1}".format(cacheFupanheziStockHistoryIdPrefix, h.id))
            df.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)