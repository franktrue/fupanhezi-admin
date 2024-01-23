from stock.models import StockSeatOffice
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class StockSeatOfficeSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockSeatOffice
        fields = '__all__'

class StockSeatOfficeCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockSeatOffice
        fields = '__all__'

class StockSeatOfficeViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockSeatOffice.objects.all()
    serializer_class = StockSeatOfficeSerializer
    create_serializer_class = StockSeatOfficeCreateUpdateSerializer
    update_serializer_class = StockSeatOfficeCreateUpdateSerializer
    filter_fields = ['seat_id', 'name']
