from coupon.models import CouponExchangeCodesModel
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.json_response import DetailResponse
from coupon.services.exchange_codes import ExchangeCodesService

class CouponExchangeCodesSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = CouponExchangeCodesModel
        fields = '__all__'

class CouponExchangeCodesCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = CouponExchangeCodesModel
        fields = '__all__'

class CouponExchangeCodesViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = CouponExchangeCodesModel.objects.all()
    serializer_class = CouponExchangeCodesSerializer
    create_serializer_class = CouponExchangeCodesCreateUpdateSerializer
    update_serializer_class = CouponExchangeCodesCreateUpdateSerializer
    filter_fields = ['exchange_id', 'key', 'user_id', 'status']
    search_fields = ['exchange_id', 'key', 'user_id', 'status']

    def create(self, request, *args, **kwargs):
        data = request.data
        service = ExchangeCodesService()
        result = service.generateCode(exchange_id=data["exchange_id"], num=data["num"])
        return DetailResponse(data=result, msg="新增成功")