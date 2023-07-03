from stock.models import StockBoardSub, StockBoardMap
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.json_response import SuccessResponse, DetailResponse
from stock.views.board_map import StockBoardMapCreateUpdateSerializer

class StockBoardSubSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockBoardSub
        fields = '__all__'

class StockBoardSubCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockBoardSub
        fields = '__all__'

class StockBoardSubViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockBoardSub.objects.all()
    serializer_class = StockBoardSubSerializer
    create_serializer_class = StockBoardSubCreateUpdateSerializer
    update_serializer_class = StockBoardSubCreateUpdateSerializer
    filter_fields = ['parent_name', 'name']
    search_fields = ['parent_name', 'name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent = serializer.data
        child_data = request.data.get("cons")
        for child in child_data:
            child["board_name"] = parent["name"]
            child["type"] = StockBoardSub.TYPE
            child["code"] = parent["name"]
            child_serializer = StockBoardMapCreateUpdateSerializer(data = child)
            child_serializer.is_valid(raise_exception=True)
            child_serializer.save()
        return DetailResponse(data=parent, msg="新增成功")
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 更新关联数据
        parent = serializer.data
        StockBoardMap.objects.filter(board_name=parent["name"]).delete()
        child_data = request.data.get("cons")
        for child in child_data:
            child["board_name"] = parent["name"]
            child["type"] = StockBoardSub.TYPE
            child["code"] = parent["name"]
            child_serializer = StockBoardMapCreateUpdateSerializer(data = child)
            child_serializer.is_valid(raise_exception=True)
            child_serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return DetailResponse(data=parent, msg="更新成功")
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        StockBoardMap.objects.filter(board_name=instance.name).delete()
        instance.delete()
        return DetailResponse(data=[], msg="删除成功")