from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from dvadmin.utils.json_response import DetailResponse
from stock.services.info import StockInfoService

class StockInfoAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        stock_code = request.data.get('stock_code')
        service = StockInfoService()
        info = service.info(symbol = stock_code)
        zyjs = service.zyjs(symbol = stock_code)
        gdfx_top = service.gdfx_top(symbol = stock_code)
        gdfx_free_top = service.gdfx_free_top(symbol = stock_code)
        news = service.news(symbol = stock_code)
        data = {"info": info, "zyjs": zyjs, "gdfx_top": gdfx_top, "gdfx_free_top": gdfx_free_top, "news": news}
        return DetailResponse(data=data, msg="更新成功")