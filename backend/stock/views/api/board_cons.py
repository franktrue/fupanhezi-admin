from rest_framework.views import APIView
from dvadmin.utils.json_response import DetailResponse
from stock.services.board import StockBoardService

class StockBoardConsAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        service = StockBoardService()
        data = service.cons(name=name)
        return DetailResponse(data=data, msg="获取成功")
        