from stock.models import StockHistory, StockTradeDate
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse
from stock.services.history import StockHistoryService
from stock.tasks import update_auction
import datetime

class StockHistorySerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockHistory
        fields = '__all__'

class StockHistoryCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockHistory
        fields = '__all__'

class StockHistoryViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockHistory.objects.all()
    serializer_class = StockHistorySerializer
    create_serializer_class = StockHistoryCreateUpdateSerializer
    update_serializer_class = StockHistoryCreateUpdateSerializer
    filter_fields = ['date', 'stock_code', 'stock_name', 'is_lhb']
    search_fields = ['stock_code', 'stock_name']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        stock_code = request.data.get('stock_code')
        stock_name = request.data.get('stock_name')
        fq = request.data.get('fq')
        between = request.data.get('between')
        start_date = datetime.datetime.strptime(between[0], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(between[1], '%Y-%m-%d').date()
        service = StockHistoryService()
        service.fetch(
            stock_code=stock_code, 
            stock_name=stock_name, 
            begin=start_date, 
            end=end_date, 
            fq=fq
        )
        return DetailResponse(data=[], msg="获取成功")

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def latest(self, request, *args, **kwargs):
        service = StockHistoryService()
        service.update_latest()
        return DetailResponse(data=[], msg="更新成功")
    
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def update_auction(self, request, *args, **kwargs):
        between = request.data.get('between')
        trade_date_range = StockTradeDate.objects.filter(trade_date__gte=between[0], trade_date__lte=between[1]).all()
        for trade_date in trade_date_range.iterator():
            update_auction.delay(trade_date.trade_date)
        return DetailResponse(data=[], msg="更新成功")
