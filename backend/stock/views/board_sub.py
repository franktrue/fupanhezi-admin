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
    filter_fields = ['parent_name', 'name', 'type']
    search_fields = ['parent_name', 'name', 'type']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        parent = serializer.data
        child_data = request.data.get("cons")
        if child_data is not None:
            for child in child_data:
                child["board_name"] = parent["name"]
                child["type"] = StockBoardSub.TYPE
                # 使用上级概念作为code码，方便联查
                child["code"] = parent["parent_name"]  
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
        child_data = request.data.get("cons")
        hadChild = []
        if child_data is not None:
            for child in child_data:
                model = StockBoardMap.objects.filter(board_name=parent["name"], stock_code=child["stock_code"], type=StockBoardSub.TYPE).first()
                if model is None:
                    model = StockBoardMap(
                        board_name = parent["name"],
                        type = StockBoardSub.TYPE,
                        code = parent["parent_name"],
                        stock_code = child['stock_code'],
                        stock_name = child['stock_name']
                    )
                else:
                    model.code = parent["parent_name"]
                model.save()
                hadChild.append(model.stock_code)
        StockBoardMap.objects.filter(board_name=parent["name"]).exclude(stock_code__in=hadChild).delete()
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