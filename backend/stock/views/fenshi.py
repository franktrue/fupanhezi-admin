from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from dvadmin.utils.json_response import DetailResponse
from stock.services.fenshi import StockFenshiService

class StockFenshiAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        stock_code = request.data.get('stock_code')
        date = request.data.get('date')
        service = StockFenshiService()
        data = service.data(stock_code=stock_code, date_str=date)
        return DetailResponse(data=data, msg="更新成功")