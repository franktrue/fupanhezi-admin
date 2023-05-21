from stock.models import StockBoardConcept
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse
from stock.services.board import StockBoardService

class StockBoardConceptSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockBoardConcept
        fields = '__all__'

class StockBoardConceptCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockBoardConcept
        fields = '__all__'

class StockBoardConceptViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockBoardConcept.objects.all()
    serializer_class = StockBoardConceptSerializer
    create_serializer_class = StockBoardConceptCreateUpdateSerializer
    update_serializer_class = StockBoardConceptCreateUpdateSerializer
    filter_fields = ['code', 'name']
    search_fields = ['code', 'name']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        service = StockBoardService()
        service.fetch_concept()
        return SuccessResponse(data=[], msg="获取成功")
