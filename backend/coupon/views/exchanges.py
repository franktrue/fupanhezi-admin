from coupon.models import CouponExchangesModel
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.json_response import DetailResponse
from stock.utils.cache import delete_cache_by_key
from coupon.utils.tool import generate_exchange_code
from coupon.services.exchange_codes import ExchangeCodesService


class CouponExchangesSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = CouponExchangesModel
        fields = '__all__'

class CouponExchangesCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = CouponExchangesModel
        fields = '__all__'

class CouponExchangesViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = CouponExchangesModel.objects.all()
    serializer_class = CouponExchangesSerializer
    create_serializer_class = CouponExchangesCreateUpdateSerializer
    update_serializer_class = CouponExchangesCreateUpdateSerializer
    filter_fields = ['name', 'del_flag']
    search_fields = ['name', 'del_flag']
    cache_key = "cache:fupanhezi:couponExchanges:id:"

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        if data["type"] == "many":
            data["code"] = generate_exchange_code(10)

        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        res = serializer.data
        if data["type"] == "only":
            service = ExchangeCodesService()
            service.generateCode(exchange_id=res["id"], num=data["total_count"])
        return DetailResponse(data=res, msg="新增成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        delete_cache_by_key("{0}{1}".format(self.cache_key, instance.id))
        return DetailResponse(data=serializer.data, msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        key = "{0}{1}".format(self.cache_key, instance.id)
        instance.delete()
        delete_cache_by_key(key)
        return DetailResponse(data=[], msg="删除成功")