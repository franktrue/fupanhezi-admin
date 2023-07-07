from stock.models import StockBoardMap
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse, DetailResponse
from stock.services.board import StockBoardService

class StockBoardMapSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockBoardMap
        fields = '__all__'

class StockBoardMapCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockBoardMap
        fields = '__all__'

class StockBoardMapViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockBoardMap.objects.all()
    serializer_class = StockBoardMapSerializer
    create_serializer_class = StockBoardMapCreateUpdateSerializer
    update_serializer_class = StockBoardMapCreateUpdateSerializer
    filter_fields = ['stock_code', 'stock_name', 'code', 'board_name', 'type']
    search_fields = ['stock_code', 'stock_name', 'code', 'board_name', 'type']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        service = StockBoardService()
        service.update_cons(
            symbol = request.data.get('code'),
            name = request.data.get('name'),
            type = request.data.get('type')
        )
        return SuccessResponse(data=[], msg="更新成功")
    
    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def dict(self, request, *args, **kwargs ):
        name = request.query_params.get('parent_name')
        print(name)
        service = StockBoardService()
        data = service.dict(name=name)
        return DetailResponse(data=data, msg="获取数据成功")
