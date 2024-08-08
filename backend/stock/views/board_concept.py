from stock.models import StockBoardConcept, StockBoardMap, StockBoardSub
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse
from stock.tasks import update_board_cons
import akshare as ak

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
        df = ak.stock_board_concept_name_ths()
        df.columns = ['release_date', 'name', 'include_number', 'show_url', 'code']
        for row in df.itertuples():
            board = StockBoardConcept.objects.filter(code=row.code).first()
            if board is None:
                board = StockBoardConcept(
                    name = row.name,
                    code = row.code,
                    release_date = row.release_date,
                    include_number = row.include_number,
                    show_url = row.show_url
                )
            elif board.include_number != row.include_number or board.name != row.name:
                board.include_number = row.include_number
                board.release_date = row.release_date
                board.name = row.name
            else:
                continue
            board.save()
            update_board_cons.apply_async((row.code, row.name, 'concept'), countdown = 4*row.Index)
        return DetailResponse(data=[], msg="获取成功")
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        StockBoardMap.objects.filter(board_name=instance.name).delete()
        StockBoardSub.objects.filter(parent_name=instance.name).delete()
        instance.delete()
        return DetailResponse(data=[], msg="删除成功")
