from stock.models import StockSeat
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from stock.services.seat import StockSeatService
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse

class StockSeatSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockSeat
        fields = '__all__'

class StockSeatCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockSeat
        fields = '__all__'

class StockSeatViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockSeat.objects.all()
    serializer_class = StockSeatSerializer
    create_serializer_class = StockSeatCreateUpdateSerializer
    update_serializer_class = StockSeatCreateUpdateSerializer
    filter_fields = ['name']

    # 同步
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        service = StockSeatService()
        service.fetch()
        return SuccessResponse(data=[], msg="获取成功")
    
    # 设置缓存
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def cache(self, request, *args, **kwargs):
        service = StockSeatService()
        service.setCache()
        return SuccessResponse(data=[], msg="获取成功")