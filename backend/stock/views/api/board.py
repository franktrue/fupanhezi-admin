from rest_framework.views import APIView
from dvadmin.utils.json_response import DetailResponse
from stock.services.board import StockBoardService
import datetime

class StockBoardAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        trade_date = datetime.datetime.strptime(request.query_params.get('date'), '%Y-%m-%d').date()
        name = request.query_params.get('name')
        num = request.query_params.get('num')
        if num is None:
            num = 10
        service = StockBoardService()
        data = service.hot(name=name, trade_date=trade_date, num = num)
        return DetailResponse(data=data, msg="获取成功")
        