from coupon.utils.tool import generate_exchange_code
from coupon.models import CouponExchangesModel, CouponExchangeCodesModel
from datetime import datetime, timedelta

class ExchangeCodesService():
    # 批量生成兑换码
    def generateCode(self, exchange_id, num=1):
        exchange = CouponExchangesModel.objects.get(id = exchange_id)
        start_time = exchange.start_time
        end_time = exchange.end_time
        if exchange.expire_type == "countdown":
            # 获取当前时间
            start_time = datetime.now()
            end_time = start_time + timedelta(days=num)
        codes = []
        for i in range(0, num):
            code = CouponExchangeCodesModel(
               key = generate_exchange_code(12),
               exchange_id = exchange_id,
               start_time = start_time,
               end_time = end_time
            )
            codes.append(code)
        result = CouponExchangeCodesModel.objects.bulk_create(codes)
        return
    