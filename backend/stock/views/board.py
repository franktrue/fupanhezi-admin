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
        service = StockBoardService()
        data = service.hot(name=name, trade_date=trade_date)
        return DetailResponse(data=data, msg="更新成功")
        