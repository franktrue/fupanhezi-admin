from rest_framework.views import APIView

from dvadmin.utils.json_response import DetailResponse
from dvadmin_pay.models import DvadminPayOrderModel
from order.services.pay import OrderPayService
from order.models import OrderGoods, OrderInfo
from datetime import datetime

class WxPayNotifyAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        service = OrderPayService()
        wxpay = service.getInstance()
        result = wxpay.callback(request.headers, request.data)
        if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
            resp = result.get('resource')
            appid = resp.get('appid')
            mchid = resp.get('mchid')
            out_trade_no = resp.get('out_trade_no')
            transaction_id = resp.get('transaction_id')
            trade_type = resp.get('trade_type')
            trade_state = resp.get('trade_state')
            trade_state_desc = resp.get('trade_state_desc')
            bank_type = resp.get('bank_type')
            attach = resp.get('attach')
            success_time = resp.get('success_time')
            payer = resp.get('payer')
            amount = resp.get('amount').get('total')
            order = OrderInfo.objects.get(order_no = out_trade_no)
            order.transaction_id = transaction_id
            order.payment_time = datetime.strptime(success_time, "%Y-%m-%dT%H:%M:%S%z")
            order.is_pay = '1'
            order.save()
            return DetailResponse(msg="支付成功")
        else:
            resp = result.get('resource')
            out_trade_no = resp.get('out_trade_no')
            amount = resp.get('amount').get('total')
            DvadminPayOrderModel.objects.filter(out_trade_no=out_trade_no).update(order_status=1, amount=amount)
            return DetailResponse(msg="支付失败")
