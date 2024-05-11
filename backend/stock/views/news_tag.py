from stock.models import StockNewsTag
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class StockNewsTagSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockNewsTag
        fields = '__all__'

class StockNewsTagCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockNewsTag
        fields = '__all__'

class StockNewsTagViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockNewsTag.objects.all()
    serializer_class = StockNewsTagSerializer
    create_serializer_class = StockNewsTagCreateUpdateSerializer
    update_serializer_class = StockNewsTagCreateUpdateSerializer
    filter_fields = ['news_id', 'name', 'desc', 'include_stocks']

