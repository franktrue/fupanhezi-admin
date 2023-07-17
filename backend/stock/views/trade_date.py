from stock.models import StockTradeDate
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse
from stock.services.trade_date import StockTradeDateService

class StockTradeDateSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockTradeDate
        fields = '__all__'

class StockTradeDateCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockTradeDate
        fields = '__all__'

class StockTradeDateViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockTradeDate.objects.all()
    serializer_class = StockTradeDateSerializer
    create_serializer_class = StockTradeDateCreateUpdateSerializer
    update_serializer_class = StockTradeDateCreateUpdateSerializer
    filter_fields = ['trade_date']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        service = StockTradeDateService()
        service.fetch()
        return SuccessResponse(data=[], msg="获取成功")

    #清除指定前缀缓存 
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def del_cache(self, request, *args, **kwargs):
        service = StockTradeDateService()
        service.clear_cache_by(prefix=request.data.get("prefix"))
        return SuccessResponse(data=[], msg="操作成功")
