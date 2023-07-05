from order.models import OrderInfo
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class OrderInfoSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderInfoCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderInfoViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoSerializer
    create_serializer_class = OrderInfoCreateUpdateSerializer
    update_serializer_class = OrderInfoCreateUpdateSerializer
    filter_fields = ['order_no', 'transaction_id', 'status', 'is_pay', 'payment_way']
    search_fields = ['order_no', 'transaction_id', 'status', 'is_pay', 'payment_way']