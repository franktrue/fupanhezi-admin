from stock.models import StockLhb
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse
from stock.services.lhb import StockLhbService
import datetime

class StockLhbSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockLhb
        fields = '__all__'

class StockLhbCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockLhb
        fields = '__all__'

class StockLhbViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockLhb.objects.all()
    serializer_class = StockLhbSerializer
    create_serializer_class = StockLhbCreateUpdateSerializer
    update_serializer_class = StockLhbCreateUpdateSerializer
    filter_fields = ['date', 'stock_code', 'stock_name']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        trade_date = datetime.datetime.strptime(request.data.get('trade_date'), '%Y-%m-%d').date()
        service = StockLhbService()
        service.fetch(trade_date=trade_date)
        return SuccessResponse(data=[], msg="获取成功")
