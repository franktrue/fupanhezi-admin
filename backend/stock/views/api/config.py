from rest_framework.views import APIView
from dvadmin.utils.json_response import DetailResponse
from application import dispatch

class StockConfigAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        key = request.query_params.get('key')
        if key != "" and (key is not None):
            data = dispatch.get_system_config_values(key=key)
        else:
            data = dispatch.get_system_config()
            data = {key: value for key, value in data.items() if key.startswith("stock")}
        return DetailResponse(data=data, msg="更新成功")