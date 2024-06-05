from stock.models import StockNews, StockNewsTag
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from stock.utils.cache import delete_cache_by_key
from dvadmin.utils.json_response import DetailResponse
from stock.services.board import StockBoardService
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class StockNewsSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockNews
        fields = '__all__'

class StockNewsCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockNews
        fields = '__all__'

class StockNewsViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockNews.objects.all()
    serializer_class = StockNewsSerializer
    create_serializer_class = StockNewsCreateUpdateSerializer
    update_serializer_class = StockNewsCreateUpdateSerializer
    filter_fields = ['title', 'content', 'type']
    cache_key = "cache:fupanhezi:stockNews:id:"
    cache_tag_key = "cache:fupanhezi:stockNewsTag:id:"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        tags = StockNewsTag.objects.filter(news_id=instance.id).all()
        for tag in tags:
            tagKey = "{0}{1}".format(self.cache_tag_key, tag.id)
            tag.delete()
            delete_cache_by_key(tagKey)

        key = "{0}{1}".format(self.cache_key, instance.id)
        instance.delete()
        delete_cache_by_key(key)
        return DetailResponse(data=[], msg="删除成功")
    
    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def boards(self, request, *args, **kwargs):
        service = StockBoardService()
        data = service.getBoards()
        return DetailResponse(data=data, msg="获取成功")
