import akshare as ak
from dateutil.relativedelta import relativedelta
from datetime import date

# 判断当前日期是否是交易日
def is_trade_date(date):
    trade_dates = ak.tool_trade_date_hist_sina()
    return date in trade_dates['trade_date'].values

# 获取上个季度最后一天
def last_day_of_last_quarter():
    # 获取当前日期
    today = date.today()

    # 计算上个季度最后一天的日期
    last_quarter = (today.month - 1) // 3
    first_day_of_last_quarter = date(today.year, 3 * last_quarter + 1, 1)
    return first_day_of_last_quarter - relativedelta(days=1)