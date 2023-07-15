from application import dispatch
from wechatpayv3 import WeChatPay, WeChatPayType
from django.conf import settings
from order.utils.unique import generate_order_number
from decimal import Decimal
from order.models import OrderGoods, OrderInfo
import json

class OrderPayService():
    
    def __init__(self) -> None:
        self.wxpay = WeChatPay(
            wechatpay_type=WeChatPayType.MINIPROG,
            mchid=dispatch.get_system_config_values("wxpay_config.MCHID"),
            private_key=open(dispatch.get_system_config_values("wxpay_config.PRIVATE_KEY")).read(),
            cert_serial_no=dispatch.get_system_config_values("wxpay_config.CERT_SERIAL_NO"),
            apiv3_key=dispatch.get_system_config_values("wxpay_config.APIV3_KEY"),
            appid=dispatch.get_system_config_values("wxpay_config.APPID"),
            notify_url=settings.WXPAY_NOTIFY_URL
        )

    def getInstance(self):
        return self.wxpay

    def execute(self,user_id, goods_id, openid):
        goods = OrderGoods.objects.get(id = goods_id)
        out_trade_no = generate_order_number(8)
        code, message = self.wxpay.pay(
            pay_type=WeChatPayType.MINIPROG,
            description=goods.name,
            out_trade_no=out_trade_no,
            amount={'total': int(Decimal(goods.payment_price) * 100)},  # 微信支付的单位是分，且必须为int类型，元转换为分=amount*100
            payer={'openid': openid}
        )
        order = OrderInfo(
            user_id=user_id,
            order_no = out_trade_no,
            payment_way = "wechat",
            is_pay = '0',
            sales_price = goods.sales_price,
            payment_price = goods.payment_price
        )
        order.save()
        return json.loads(message)
