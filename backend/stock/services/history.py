from stock.models import StockHistory
from stock.utils.db import get_engine
from stock.utils.date import is_trade_date
import pywencai
import akshare as ak
import datetime

class StockHistoryService():
    def __init__(self):
        self.engine = get_engine()
        self.table_name = StockHistory._meta.db_table

    # 获取指定日期范围指定股票的行情
    def fetch(self, stock_code, stock_name, begin, end, fq):
        stock_history = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=begin.strftime("%Y%m%d"), end_date=end.strftime("%Y%m%d"), adjust=fq)
        stock_history = stock_history[['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额','换手率', '涨跌幅', '涨跌额']]
        stock_history.columns = ['date', 'open', 'close', 'high', 'low', 'vol', 'amo', 'hs_rate', 'close_pe', 'change_amo']
        stock_history['pre_close'] = stock_history['close'] - stock_history['change_amo']
        stock_history['stock_code'] = stock_code
        stock_history['stock_name'] = stock_name
        stock_history['open_pe'] = ((stock_history['open']-stock_history['pre_close'])/stock_history['pre_close']*100).apply(lambda x: round(x, 2))
        stock_history['high_pe'] = ((stock_history['high']-stock_history['pre_close'])/stock_history['pre_close']*100).apply(lambda x: round(x, 2))
        stock_history['low_pe'] = ((stock_history['open']-stock_history['pre_close'])/stock_history['pre_close']*100).apply(lambda x: round(x, 2))
        StockHistory.objects.filter(stock_code=stock_code, date__gte=begin, date__lte=end).delete()
        stock_history.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)

    # 更新最新一天的股票行情，需交易日15点以后请求
    def update_latest(self):
        now = datetime.datetime.now()
        today = now.date()
        if is_trade_date(today) and now.hour >= 15:
            count = StockHistory.objects.filter(date=today.strftime("%Y-%m-%d")).count()
            if count > 0:
                raise Exception("今日数据已更新")
            # 收盘后的行情数据
            stock_history = ak.stock_zh_a_spot_em()
            stock_history = stock_history[['代码', '名称', '今开', '最新价', '最高', '最低', '成交量', '成交额','换手率', '涨跌幅', '涨跌额', '昨收']]
            stock_history.columns = ['stock_code', 'stock_name', 'open', 'close', 'high', 'low', 'vol', 'amo', 'hs_rate', 'close_pe', 'change_amo', 'pre_close']
            stock_history = stock_history.dropna(subset=['open', 'high', 'low', 'close'])
            stock_history['date'] = today
            stock_history['open_pe'] = ((stock_history['open']-stock_history['pre_close'])/stock_history['pre_close']*100).apply(lambda x: round(x, 2))
            stock_history['high_pe'] = ((stock_history['high']-stock_history['pre_close'])/stock_history['pre_close']*100).apply(lambda x: round(x, 2))
            stock_history['low_pe'] = ((stock_history['open']-stock_history['pre_close'])/stock_history['pre_close']*100).apply(lambda x: round(x, 2))
            auction = self.get_auction(date=today)
            # 合并集合竞价数据
            stock_history = stock_history.set_index('stock_code').join(auction).reset_index()
            StockHistory.objects.filter(date=today.strftime("%Y-%m-%d")).delete()
            stock_history.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)
        else:
            raise Exception("请在交易日15点后更新数据")
        
    def get_auction(self, date):
        trade_date_str = date.strftime('%Y%m%d')
        col_name = [
            "code", 
            "竞价金额[{0}]".format(trade_date_str), 
            "竞价量[{0}]".format(trade_date_str),
            "竞价未匹配金额[{0}]".format(trade_date_str),
            "竞价未匹配量[{0}]".format(trade_date_str),
            "竞价异动类型[{0}]".format(trade_date_str),
            "竞价异动说明[{0}]".format(trade_date_str),
        ]
        auction = pywencai.get(question="{0}竞价金额 {0}竞价量".format(trade_date_str), loop=True)
        auction = auction[col_name]
        auction.columns = ['stock_code', 'auction_amo', 'auction_vol', 'auction_no_match_amo', 'auction_no_match_vol', 'auction_type', 'auction_explain']
        auction.fillna({
            'auction_amo': 0, 
            'auction_vol': 0, 
            'auction_no_match_amo': 0, 
            'auction_no_match_vol':0, 
            'auction_type': '', 
            'auction_explain': ''
        }, inplace=True)
        return auction.set_index('stock_code')

    def update_auction_by_date(self, date):
        auction = self.get_auction(date)
        for row in auction[~auction['auction_amo'].isna()].itertuples():
            StockHistory.objects.filter(stock_code=row.Index, date=date.strftime("%Y-%m-%d")).update(
                auction_vol = row.auction_vol,
                auction_amo = row.auction_amo,
                auction_no_match_vol = row.auction_no_match_vol,
                auction_no_match_amo = row.auction_no_match_amo,
                auction_type = row.auction_type,
                auction_explain = row.auction_explain
            )
        