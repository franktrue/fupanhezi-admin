from stock.models import StockZtHistory
from stock.utils.db import get_engine
from stock.utils.date import is_trade_date
import akshare as ak
import pywencai
import pandas as pd

class StockZtHistoryService():
    def __init__(self):
        self.engine = get_engine()
        self.table_name = StockZtHistory._meta.db_table
        # 日期窗口范围
        self.k = 20

    # 更新指定交易日涨停板数据
    # 同时修改之前数据中的sort数据
    def fetch(self, date):
        if is_trade_date(date):
            # 获取窗口日期
            trade_date = ak.tool_trade_date_hist_sina()
            trade_date_range = trade_date[trade_date['trade_date']<=date].tail(self.k)["trade_date"].to_list()
            # 当前日期的涨停板及炸板数据
            zt_pool = self.get_zt_history(trade_date=date)
            # 去除重复
            zt_pool.drop_duplicates(subset="stock_code", keep='first', inplace=True)
            # 前一天的涨停板及炸板数据
            pre_trade_date = trade_date_range[-2]
            pre_zt_pool = self.get_zt_history(trade_date=pre_trade_date)
            zt_pool.loc[zt_pool['ztlb_num'] == 1, 'sort'] = 1
            for zt_stock in zt_pool.itertuples():
                if zt_stock.ztlb_num >= 1:
                    head_trade_date = trade_date_range[-1*int(zt_stock.ztlb_num)]
                    sort = zt_stock.ztlb_num
                    zt_pool.loc[zt_pool['stock_code']==zt_stock.stock_code, 'sort'] = sort
                else: # 炸板
                    # 查看前一天数据是否存在
                    pre_zt_stock = pre_zt_pool.loc[pre_zt_pool['stock_code']==zt_stock.stock_code, 'ztlb_num']
                    if pre_zt_stock.empty or pre_zt_stock.values[0] < 0: # 昨日不存在或昨日炸板
                        zt_pool.loc[zt_pool['stock_code']==zt_stock.stock_code, 'sort'] = 0.5
                        continue
                    else:
                        ztlb_num = pre_zt_stock.values[0]
                        head_trade_date = trade_date_range[-1*int(ztlb_num+1)]
                        sort = ztlb_num + 0.5 # 今日炸板起始日期+0.5
                        zt_pool.loc[zt_pool['stock_code']==zt_stock.stock_code, 'sort'] = sort
                # 增加梯队排序
                StockZtHistory.objects.filter(date=head_trade_date.strftime("%Y-%m-%d"),stock_code=zt_stock.stock_code).update(sort=sort)
                print("更新{0}，日期{1}排序为{2}".format(zt_stock.stock_name, head_trade_date, sort)) 
            StockZtHistory.objects.filter(date=date.strftime("%Y-%m-%d")).delete()
            zt_pool.fillna({
                'fb_amount': 0,
                'first_zt_time': '',
                'last_zt_time': '',
                'zb_num': 0,
                'zt_statistics': '',
                'ztlb_num': 0,
                'sort': 0,
                'z_sz': 0,
                'lt_sz': 0,
                'zs_sz': 0,
                'hs_rate': 0,
                'real_hs_rate': 0,
                'pe': 0,
                'zt_type': '',
                'zt_reson': ''
            }, inplace=True)
            zt_pool.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)

    # 获取指定交易日涨停及曾涨停数据
    def get_zt_history(self, trade_date):
        trade_date_str = trade_date.strftime("%Y%m%d")
        # 涨停
        zt_pool_col_zh = [
            "code", 
            "股票简称", 
            "涨停封单额[{0}]".format(trade_date_str), 
            "首次涨停时间[{0}]".format(trade_date_str), 
            "最终涨停时间[{0}]".format(trade_date_str), 
            "涨停开板次数[{0}]".format(trade_date_str), 
            "几天几板[{0}]".format(trade_date_str), 
            "连续涨停天数[{0}]".format(trade_date_str), 
            "总市值[{0}]".format(trade_date_str),
            "a股市值(不含限售股)[{0}]".format(trade_date_str),
            "自由流通市值[{0}]".format(trade_date_str),
            # "换手率[{0}]".format(trade_date_str),
            "实际换手率[{0}]".format(trade_date_str),
            "市盈率(pe)[{0}]".format(trade_date_str),
            # "基本每股收益[{0}]".format(trade_date_str),
            "涨停类型[{0}]".format(trade_date_str),
            "涨停原因类别[{0}]".format(trade_date_str)
        ]
        zt_pool_col = ['stock_code', 'stock_name', 'fb_amount', 'first_zt_time', 'last_zt_time', 'zb_num', 'zt_statistics', 'ztlb_num', 'z_sz', 'lt_sz', 'zs_sz', 'real_hs_rate', 'pe', 'zt_type', 'zt_reson']
        question = "{0}涨停板 {0}总市值 {0}流通市值 {0}自由流通市值 {0}实际换手率 {0}市盈率 {0}涨停类型 {0}涨停原因".format(trade_date_str)
        zt_pool = pywencai.get(question=question, loop=True)
        zt_pool = zt_pool[zt_pool_col_zh]
        zt_pool.columns = zt_pool_col
        zt_pool['date'] = trade_date
        # 炸板
        zb_pool_col_zh = [
            "code", 
            "股票简称", 
            "首次涨停时间[{0}]".format(trade_date_str), 
            "涨停开板次数[{0}]".format(trade_date_str), 
            "几天几板[{0}]".format(trade_date_str), 
            "总市值[{0}]".format(trade_date_str),
            "a股市值(不含限售股)[{0}]".format(trade_date_str),
            "自由流通市值[{0}]".format(trade_date_str),
            # "换手率[{0}]".format(trade_date_str),
            "实际换手率[{0}]".format(trade_date_str),
            "市盈率(pe)[{0}]".format(trade_date_str),
        ]
        zb_pool_col = ['stock_code', 'stock_name', 'first_zt_time', 'zb_num', 'zt_statistics', 'z_sz', 'lt_sz', 'zs_sz', 'real_hs_rate', 'pe']
        zb_pool = pywencai.get(question="{0}曾涨停 首次涨停时间 涨停开板次数 几天几板 {0}总市值 {0}流通市值 {0}自由流通市值 {0}实际换手率 {0}市盈率".format(trade_date_str), loop=True)
        zb_pool = zb_pool[zb_pool_col_zh]
        zb_pool.columns = zb_pool_col
        zb_pool['date'] = trade_date
        zb_pool['ztlb_num'] = -1
        df = pd.concat([zt_pool, zb_pool], axis=0, ignore_index=True)
        return df