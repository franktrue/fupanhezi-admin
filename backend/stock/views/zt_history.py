from stock.models import StockZtHistory
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse
from stock.services.zt_history import StockZtHistoryService
import datetime

class StockZtHistorySerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockZtHistory
        fields = '__all__'

class StockZtHistoryCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockZtHistory
        fields = '__all__'

class StockZtHistoryViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockZtHistory.objects.all()
    serializer_class = StockZtHistorySerializer
    create_serializer_class = StockZtHistoryCreateUpdateSerializer
    update_serializer_class = StockZtHistoryCreateUpdateSerializer
    filter_fields = ['date', 'stock_code', 'stock_name', 'ztlb_num']
    search_fields = ['stock_code', 'stock_name']
    
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        trade_date = datetime.datetime.strptime(request.data.get('trade_date'), '%Y-%m-%d').date()
        service = StockZtHistoryService()
        service.fetch(date=trade_date)
        return SuccessResponse(data=[], msg="获取成功")