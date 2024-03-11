from stock.models import StockHistory, StockLhb
from stock.utils.db import get_engine
from stock.utils.date import is_trade_date
from django_redis import get_redis_connection
from stock.services.seat import StockSeatService
import pandas as pd
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
            df = df[['序号', '代码', '名称', '解读', '收盘价', '涨跌幅', '龙虎榜净买额', '龙虎榜买入额',
                '龙虎榜卖出额', '龙虎榜成交额', '市场总成交额', '净买额占总成交比', '成交额占总成交比', '换手率', '流通市值', '上榜原因']]
            df.columns = ["serial", "stock_code", "stock_name", "interpretation", "close", "close_pe", "lhb_net_buy_amo", "lhb_buy_amo", "lhb_sell_amo", "lhb_amo", "market_total_amo", "net_buy_amo_pe", "amo_pe", "hs_rate", "circulate_market_value", "rank_reson"]
            df["date"] = trade_date
            df.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)

            redis_conn = get_redis_connection('default')
            cacheFupanheziStockHistoryIdPrefix = "cache:fupanhezi:stockHistory:id:"
            df2 = pd.DataFrame()
            # 去重
            df.drop_duplicates(subset="stock_code")

            service = StockSeatService()
            for row in df.itertuples():
                # 更新数据中的涨停板
                if row.interpretation is None:
                    interpretation = ''
                else:
                    interpretation = row.interpretation
                h = StockHistory.objects.filter(stock_code=row.stock_code, date=trade_date.strftime("%Y-%m-%d")).first()
                if h is not None:
                    h.lhb_parse = interpretation
                    h.lhb_reson = h.lhb_reson + " | "+ row.rank_reson
                    if "三个交易日" in row.rank_reson:
                        h.is_lhb += 3
                    else:
                        h.is_lhb += 1
                    h.save()
                    redis_conn.delete("{0}{1}".format(cacheFupanheziStockHistoryIdPrefix, h.id))
                # 记录买入/卖出席位
                try:
                    item1 = ak.stock_lhb_stock_detail_em(symbol=row.stock_code, date=date_str, flag="买入")
                    item1["type"] = "buy"
                except Exception:
                    item1 = pd.DataFrame()
                
                try:
                    item2 = ak.stock_lhb_stock_detail_em(symbol=row.stock_code, date=date_str, flag="卖出")
                    item2["type"] = "sell"
                except Exception:
                    item2 = pd.DataFrame()

                items = pd.concat([item1, item2], axis=0, ignore_index=True)
                items.columns = ["sort", "office", "buy_amount", "buy_rate", "sell_amount", "sell_rate", "net_amount", "desc", "type"]
                items["date"] = trade_date
                items["stock_code"] = row.stock_code
                items["seat"] = ""
                # 添加席位名称
                for v in items.itertuples():
                    seat = service.getByOffice(v.office)
                    if seat is not None:
                        items.loc[items["office"] == v.office, "seat"] = seat
                df2 = pd.concat([df2, items], axis=0, ignore_index=True)
            df2.fillna({
                "sell_amount": 0, 
                "buy_amount": 0,
                "sell_rate": 0,
                "buy_rate": 0
            }, inplace=True)
            df2.to_sql(name="stock_lhb_item", con=self.engine, if_exists="append", index=False)
            self.engine.dispose()