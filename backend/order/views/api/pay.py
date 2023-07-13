from rest_framework.views import APIView
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from order.services.pay import OrderPayService

class OrderPaymentAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        goods_id = request.data.get('goods_id')
        openid = request.data.get('openid')
        service = OrderPayService()
        result = service.execute(user_id=user_id, goods_id=goods_id, openid=openid)
        if "code" in result.keys():
            return ErrorResponse(msg=result['message'])
        return DetailResponse(data=result, msg="OK")