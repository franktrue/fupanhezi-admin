from stock.models import StockBoardHistory, StockTradeDate
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse
from stock.services.board import StockBoardService
from stock.tasks import update_board_history
import datetime

class StockBoardHistorySerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockBoardHistory
        fields = '__all__'

class StockBoardHistoryCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockBoardHistory
        fields = '__all__'

class StockBoardHistoryViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockBoardHistory.objects.all()
    serializer_class = StockBoardHistorySerializer
    create_serializer_class = StockBoardHistoryCreateUpdateSerializer
    update_serializer_class = StockBoardHistoryCreateUpdateSerializer
    filter_fields = ['name', 'date']
    search_fields = ['name', 'date']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch_all(self, request, *args, **kwargs):
        between = request.data.get('between')
        trade_date_range = StockTradeDate.objects.filter(trade_date__gte=between[0], trade_date__lte=between[1]).all()
        for trade_date in trade_date_range.iterator():
            update_board_history.delay(trade_date.trade_date.strftime('%Y-%m-%d'))
        return DetailResponse(data=[], msg="更新成功")
    
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        trade_date = datetime.datetime.strptime(request.data.get('trade_date'), '%Y-%m-%d').date()
        service = StockBoardService()
        service.fetch_history(trade_date=trade_date)
        return DetailResponse(data=[], msg="更新成功")