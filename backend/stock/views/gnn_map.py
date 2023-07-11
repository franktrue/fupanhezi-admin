from stock.models import StockGnnMap
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse
from stock.services.gnn import StockGnnService

class StockGnnMapSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockGnnMap
        fields = '__all__'

class StockGnnMapCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockGnnMap
        fields = '__all__'

class StockGnnMapViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockGnnMap.objects.all()
    serializer_class = StockGnnMapSerializer
    create_serializer_class = StockGnnMapCreateUpdateSerializer
    update_serializer_class = StockGnnMapCreateUpdateSerializer
    filter_fields = ['stock_code', 'stock_name', 'code', 'name', 'type']
    search_fields = ['stock_code', 'stock_name', 'code', 'name', 'type']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        service = StockGnnService()
        service.syncCons(code = request.data.get('code'), name=request.data.get('name'))
        return DetailResponse(data=[], msg="更新成功")
