from stock.models import StockHistory, StockLhb
from stock.utils.db import get_engine
from stock.utils.date import is_trade_date
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
            for row in df.itertuples():
                # 更新数据中的涨停板
                if row.interpretation is None:
                    interpretation = ''
                else:
                    interpretation = row.interpretation
                StockHistory.objects.filter(stock_code=row.stock_code, date=trade_date.strftime("%Y-%m-%d")).update(
                    is_lhb=1, 
                    lhb_parse=interpretation,
                    lhb_reson=row.rank_reson
                )
            df.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)