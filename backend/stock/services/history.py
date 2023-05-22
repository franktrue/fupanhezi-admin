from stock.models import StockHistory
from stock.utils.db import get_engine
from stock.utils.date import is_trade_date
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
            StockHistory.objects.filter(date=today.strftime("%Y-%m-%d")).delete()
            stock_history.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)
        else:
            raise Exception("请在交易日15点后更新数据")