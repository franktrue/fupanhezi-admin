from stock.models import StockBoardConcept, StockBoardIndustry, StockBoardMap, StockBoardHistory, StockGnnMap,StockBoardSub
from stock.utils.db import get_engine
from django.db import connections
from django.core.cache import cache
import datetime
import akshare as ak
import pywencai

class StockBoardService():
    def __init__(self):
        self.engine = get_engine()
        self.timeout = 24*3600

    # 更新概念
    def fetch_concept(self):
        df = ak.stock_board_concept_name_ths()
        df.columns = ['release_date', 'name', 'include_number', 'show_url', 'code']
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(StockBoardConcept._meta.db_table))
        df.to_sql(name=StockBoardConcept._meta.db_table, con=self.engine, if_exists="append", index=False)

    # 更新行业
    def fetch_industry(self):
        df = ak.stock_board_industry_name_ths()
        with connections['default'].cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {0}'.format(StockBoardIndustry._meta.db_table))
        df.to_sql(name=StockBoardIndustry._meta.db_table, con=self.engine, if_exists="append", index=False)
        return df
    
    # 更新成分股
    def update_cons(self, symbol, name, type):
        df = ak.stock_board_cons_ths(symbol=symbol)
        df = df[['代码', '名称']]
        df.columns = ['stock_code', 'stock_name']
        df['code'] = symbol
        df['board_name'] = name
        df['type'] = type
        # 先删除旧数据
        StockBoardMap.objects.filter(code=symbol).delete()
        df.to_sql('stock_board_map', con=self.engine, if_exists="append", index=False)

    # 更新板块行情
    def fetch_history(self, trade_date, type = None):
        trade_date_str = trade_date.strftime("%Y%m%d")
        df=pywencai.get(question="同花顺板块指数{0}开盘价 {0}最高价 {0}最低价 {0}收盘价 {0}涨跌幅 {0}成交额成交量换手率".format(trade_date_str), query_type="zhishu", loop=True)
        # 包含概念和行业
        df = df[(df["指数@同花顺板块指数"]=="同花顺概念指数") | (df["指数@同花顺板块指数"]=="同花顺行业指数")]
        col_zh = [
            "code", 
            "指数简称", 
            "指数@开盘价:不复权[{0}]".format(trade_date_str), 
            "指数@最高价:不复权[{0}]".format(trade_date_str), 
            "指数@最低价:不复权[{0}]".format(trade_date_str), 
            "指数@收盘价:不复权[{0}]".format(trade_date_str), 
            "指数@涨跌幅:前复权[{0}]".format(trade_date_str), 
            "指数@成交额[{0}]".format(trade_date_str), 
            "指数@成交量[{0}]".format(trade_date_str),
            "指数@换手率[{0}]".format(trade_date_str),
            "指数@同花顺板块指数",
        ]
        df = df[col_zh]
        df.columns = ['code', 'name', 'open', 'high', 'low', 'close', 'close_pe', 'vol', 'amo', 'hs_rate', 'type']
        df = df[~df['open'].isna()]
        df['type'] = df['type'].replace('同花顺概念指数', 'concept').replace('同花顺行业指数', 'industry')
        df['date'] = trade_date
        if type is not None :
            df = df[df['type'] == type]
            StockBoardHistory.objects.filter(date=trade_date, type=type).delete()
        else:
            StockBoardHistory.objects.filter(date=trade_date).delete()
        df.to_sql(name=StockBoardHistory._meta.db_table, con=self.engine, if_exists="append", index=False)

    def fetch_history_by_task(self, trade_date):
        trade_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d').date()
        self.fetch_history(trade_date=trade_date)

    # 指定日期板块热门股
    def hot(self, name, trade_date, num):
        trade_date_str = trade_date.strftime("%Y%m%d")
        key = "stock_board_hot:{0}:{1}:{2}".format(name, trade_date_str, num)
        data = cache.get(key)
        if data is None:
            if "概念" not in name:
                name += "概念"
            df=pywencai.get(question="{0}{1}成分股个股热度前{2}名 {0}成交量 {0}真实流通市值 {0}换手率及真实换手率 {0}收盘价涨幅".format(trade_date_str, name, num), loop=True)
            if df.empty:
                return data
            col_zh = [
                "code", 
                "股票简称",
                "开盘价:前复权[{0}]".format(trade_date_str), 
                "最高价:前复权[{0}]".format(trade_date_str), 
                "最低价:前复权[{0}]".format(trade_date_str), 
                "收盘价:前复权[{0}]".format(trade_date_str), 
                "涨跌幅:前复权[{0}]".format(trade_date_str), 
                "成交量[{0}]".format(trade_date_str), 
                "成交额[{0}]".format(trade_date_str),
                "换手率[{0}]".format(trade_date_str),
                "实际换手率[{0}]".format(trade_date_str),
                "自由流通市值[{0}]".format(trade_date_str),
            ]
            df = df[col_zh]
            df.columns = ['code', 'name', 'open', 'high', 'low', 'close', 'closePe', 'vol', 'amo', 'hsRate', 'realHsRate', 'zsSz']
            df[['closePe', 'hsRate', 'realHsRate']] = df[['closePe', 'hsRate', 'realHsRate']].astype(float).applymap(lambda x: round(x, 2))
            data = df.to_dict("records")
            cache.set(key, data, timeout=self.timeout)
        return data
       
    # 指定板块成分股
    def cons(self, name):
        key = "stock_board_cons:{0}".format(name)
        data = cache.get(key)
        if data is None:
            if "概念" not in name:
                name += "概念"
            df=pywencai.get(question="{0}成分股 真实流通市值".format(name))
            if df.empty:
                return data
            today = datetime.date.today()
            trade_date_str = today.strftime("%Y%m%d")
            col_zh = [
                "code", 
                "股票简称",
                "最新价", 
                "最新涨跌幅", 
                "概念解析", 
                "所属指数类", 
                "所属概念数量",
                "自由流通市值[{0}]".format(trade_date_str),
                "a股市值(不含限售股)[{0}]".format(trade_date_str),
                "实际换手率[{0}]".format(trade_date_str),
            ]
            df = df[col_zh]
            df.columns = ['code', 'name', 'price', 'price_pe', 'parse', 'indexs', 'conceptNum', "zsSz", "zSz", "realHsRate"]
            df['realHsRate'] = df['realHsRate'].round(2)
            data = df.to_dict("records")
            cache.set(key, data, timeout=self.timeout)
        return data

    def dict(self, name):
        rows = StockBoardMap.objects.filter(board_name=name).all()
        data = []
        for row in rows:
            v = row.stock_code + " " + row.stock_name
            data.append({
                "value": v,
                "label": v
            })
        return data

    # 批量转化
    def batch(self, name, ids):
        code, name = name.split("/")
        result = StockGnnMap.objects.filter(id__in=ids)
        for item in result:
            model = StockBoardMap.objects.filter(board_name=name, stock_code = item.stock_code).first()
            if model is None:
                model = StockBoardMap(
                    code = code,
                    board_name = name,
                    stock_code = item.stock_code,
                    stock_name = item.stock_name,
                    brief = item.brief,
                    type = StockBoardSub.TYPE
                )
            else:
                model.code = name
                model.brief = item.brief
            model.save()
