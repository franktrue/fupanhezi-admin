from stock.models import StockBoardHistory
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse
from stock.services.board import StockBoardService

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
    def fetch(self, request, *args, **kwargs):
        service = StockBoardService()
        service.fetch_history(symbol = request.data.get('name'))
        return SuccessResponse(data=[], msg="更新成功")