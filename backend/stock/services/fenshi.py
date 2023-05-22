from stock.models import StockHistory
from django.core.cache import cache
import urllib.parse
import urllib.request
import csv
import datetime

class StockFenshiService():

    def data(self, stock_code, date_str):
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        key = stock_code+date_str
        data = cache.get(key)
        if data is None:
            # 判断是上证还是深证
            if  stock_code[0] == '6':
                full_stock_code = 'SH#' + stock_code
            else:
                full_stock_code = 'SZ#' + stock_code
            reader = self.read_csv_by_date(full_stock_code=full_stock_code, dir=self.date_to_quarter(date))
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
                    pre_close = round(open_price/(1+h.open_pe/100), 2)
                    break
            data = {"pre_close": pre_close, "open_price": open_price, "list": list}
            cache.set(key, data, timeout=24*3600)
        return data
        
    def read_csv_by_date(self, full_stock_code, dir):
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
    