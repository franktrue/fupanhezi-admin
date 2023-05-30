from rest_framework.views import APIView
from dvadmin.utils.json_response import DetailResponse
from stock.services.fenshi import StockFenshiService

class StockFenshiAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        stock_code = request.data.get('stock_code')
        date = request.data.get('date')
        service = StockFenshiService()
        data = service.data(stock_code=stock_code, date_str=date)
        return DetailResponse(data=data, msg="更新成功")