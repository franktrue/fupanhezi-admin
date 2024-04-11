from stock.models import StockSeat
from django_redis import get_redis_connection
import tushare as ts

class StockSeatService():
    def __init__(self):
        self.cache_key = "seats"
        self.redis_conn = get_redis_connection('default')

    # 获取游资名录
    def fetch(self):
        # 18611394471账号token
        # 3a81403adc5d6f7bbf59a9b6f104931af2bd9f4f23ac216386526299
        ts.set_token('6e1f4c7c734da81d39b571b8612a941484c1b2d97a23d580733600f7')
        pro = ts.pro_api()
        df = pro.hm_list()
        seats = []
        # 先清空
        names = StockSeat.objects.values_list('name', flat=True)
        df = df[~df['name'].isin(names)]
        for v in df.itertuples():
            seat = StockSeat(
                name = v.name,
                short_name = v.name,
                description = v.desc,
                offices = v.orgs[1:-1].replace('"', ""),
                sort = 0
            )
            seats.append(seat)
        if len(seats):
            # 插入最新
            result = StockSeat.objects.bulk_create(seats)
            # 更新缓存
            self.setCache()
            return result

    # 获取对应席位
    def getByOffice(self, office):
        return self.redis_conn.hget(self.cache_key, office)
        
    # 设置缓存
    def setCache(self):
        self.redis_conn.delete(self.cache_key)
        res = StockSeat.objects.all()
        for v in res:
            for i in v.offices.split(", "):
                self.redis_conn.hset(self.cache_key, i, v.name + '|' + v.short_name)
