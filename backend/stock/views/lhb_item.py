from stock.models import StockLhbItem
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class StockLhbItemSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockLhbItem
        fields = '__all__'

class StockLhbItemCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockLhbItem
        fields = '__all__'

class StockLhbItemViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockLhbItem.objects.all()
    serializer_class = StockLhbItemSerializer
    create_serializer_class = StockLhbItemCreateUpdateSerializer
    update_serializer_class = StockLhbItemCreateUpdateSerializer
    filter_fields = ['date', 'stock_code', 'office']

