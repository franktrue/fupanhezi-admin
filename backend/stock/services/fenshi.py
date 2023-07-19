from stock.models import StockHistory
from django.core.cache import cache
from stock.utils.tencent import Tencent
import pandas as pd
import io
import urllib.parse
import urllib.request
import csv
import datetime
import akshare as ak

class StockFenshiService():

    def data(self, stock_code, date_str):
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        key = "stock_fenshi:"+stock_code+date_str
        data = cache.get(key)
        if data is None:
            full_stock_code = self.get_full_stock_code(stock_code=stock_code)
            reader = self.read_csv_by_date(full_stock_code=full_stock_code, date=date)
            list = []
            pre_close = None
            open_price = None
            i = 0
            vol = 0
            amo = 0
            for row in reader:
                if row[0] == date_str:
                    if i == 0:
                        open_price = float(row[2])
                    vol = vol + int(row[6])
                    amo = amo + float(row[7])
                    list.append({
                        "moment": row[1],
                        "price": float(row[5]),
                        "avg_price": round(amo / vol, 4),
                        "vol": int(row[6]),
                        "amo": float(row[7])
                    })
                    i = i+1
                # 一天分时240行
                if i == 240:
                    h =  StockHistory.objects.get(stock_code=stock_code, date = date_str)
                    if h is None:
                        return None
                    pre_close = round(open_price/(1+h.open_pe/100), 2)
                    break
            data = {"pre_close": pre_close, "open_price": open_price, "list": list}
            if len(list)>0:
                cache.set(key, data, timeout=24*3600)
        return data
    
    def get_full_stock_code(self, stock_code):
        # 判断是上证还是深证
        if  stock_code[0] == '6':
            return 'SH#' + stock_code
        else:
            return 'SZ#' + stock_code
        
    def read_csv_by_date(self, full_stock_code, date):
        # 当前日期开始以天为单位上传分时数据
        date_str = date.strftime("%Y-%m-%d")
        if date_str >= "2023-07-19":
            dir = date_str+"/"
        else:
            dir = self.date_to_quarter(date)
        url = "https://stock-fenshi-1302497504.cos.ap-shanghai.myqcloud.com/"+dir+urllib.parse.quote(full_stock_code)+".csv"
        response = urllib.request.urlopen(url)
        # 读取 CSV 文件内容
        lines = [l.decode('gb2312').strip() for l in response.readlines()]
        return csv.reader(lines)
    
    def date_to_quarter(self,  date):
        year = date.year
        month = date.month
        quarter = (month - 1) // 3 + 1
        quarter_str = f'Q{quarter}'
        return f"{year}/{quarter_str}/"
    
    # 同步股票分时数据到腾讯云COS
    def sync(self, stock_code, date):
        df = ak.stock_zh_a_hist_min_em(symbol=stock_code, start_date="{0} 09:30:00".format(date), end_date="{0} 15:00:00".format(date), period='1', adjust='')
        if df.empty:
            return
        df["日期"] = pd.to_datetime(df["时间"]).dt.date
        df["时间"] = pd.to_datetime(df["时间"]).dt.strftime('%H%M')
        # 1手=100股
        df["成交量"] = df["成交量"]*100
        df=df[["日期", "时间", "开盘", "最高", "最低", "收盘", "成交量", "成交额"]]
        csv_bytes = io.BytesIO()
        df.to_csv(csv_bytes, index=False, encoding="gb2312")
        csv_bytes.seek(0)

        tencent = Tencent()
        cos_client = tencent.get_cos_client()
        full_stock_code = self.get_full_stock_code(stock_code=stock_code)
        file_name = "{0}/{1}.csv".format(date, full_stock_code)
        cos_client.put_object(Bucket="stock-fenshi-1302497504", Body=csv_bytes, Key=file_name)