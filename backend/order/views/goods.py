from order.models import OrderGoods
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class OrderGoodsSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = OrderGoods
        fields = '__all__'

class OrderGoodsCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = OrderGoods
        fields = '__all__'

class OrderGoodsViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = OrderGoods.objects.all()
    serializer_class = OrderGoodsSerializer
    create_serializer_class = OrderGoodsCreateUpdateSerializer
    update_serializer_class = OrderGoodsCreateUpdateSerializer
    filter_fields = ['name', 'del_flag']
    search_fields = ['name', 'del_flag']