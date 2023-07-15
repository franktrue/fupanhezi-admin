from order.models import OrderItem
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class OrderItemSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    create_serializer_class = OrderItemCreateUpdateSerializer
    update_serializer_class = OrderItemCreateUpdateSerializer
    filter_fields = ['order_info_id', 'spu_name', 'status']
    search_fields = ['order_info_id', 'spu_name', 'status']