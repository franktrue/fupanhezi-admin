from coupon.models import CouponExchangeCodesModel
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.json_response import DetailResponse
from coupon.services.exchange_codes import ExchangeCodesService
from rest_framework import serializers

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

class CouponExchangeCodesImportSerializer(CustomModelSerializer):  
    status_label=serializers.CharField(source='get_status_display', read_only=True,  help_text='状态')   
    dept_name = serializers.CharField(source='dept.name', read_only=True, default=None, help_text='部门名称')  
    create_datetime = serializers.DateField(required=False, help_text="创建时间")

    class Meta:  
        model = CouponExchangeCodesModel  
        fields = "__all__"  
        read_only_fields = ["id"]

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
    export_field_label = {  
        "key": "兑换码",
        "start_time": "开始时间",
        "end_time": "结束时间"
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        service = ExchangeCodesService()
        result = service.generateCode(exchange_id=data["exchange_id"], num=data["num"])
        return DetailResponse(data=result, msg="新增成功")