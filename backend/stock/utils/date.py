import akshare as ak

# 判断当前日期是否是交易日
def is_trade_date(date):
    trade_dates = ak.tool_trade_date_hist_sina()
    return date in trade_dates['trade_date'].values