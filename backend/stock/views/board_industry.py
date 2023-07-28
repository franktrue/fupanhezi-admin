from stock.models import StockBoardIndustry
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse
from stock.tasks import update_board_cons
import akshare as ak

class StockBoardIndustrySerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = StockBoardIndustry
        fields = '__all__'

class StockBoardIndustryCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = StockBoardIndustry
        fields = '__all__'

class StockBoardIndustryViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockBoardIndustry.objects.all()
    serializer_class = StockBoardIndustrySerializer
    create_serializer_class = StockBoardIndustryCreateUpdateSerializer
    update_serializer_class = StockBoardIndustryCreateUpdateSerializer
    filter_fields = ['code', 'name']
    search_fields = ['code', 'name']

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request, *args, **kwargs):
        df = ak.stock_board_industry_name_ths()
        for row in df.itertuples():
            # 每隔任务间隔4s防止触发保护机制
            update_board_cons.apply_async((row.code, row.name, 'industry'), countdown = 4*row.Index)
        return DetailResponse(data=[], msg="获取成功")
    