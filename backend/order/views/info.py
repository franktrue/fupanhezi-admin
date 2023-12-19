from order.models import OrderInfo
from user_center.models import UserCoupon
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework import serializers

class OrderInfoSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = OrderInfo
        fields = '__all__'

    user_coupon_name = serializers.SerializerMethodField()

    def get_user_coupon_name(self, instance):
        if instance.user_coupon_id > 0 :
            res =  UserCoupon.objects.filter(id=instance.user_coupon_id).first()
            if res is not None:
                return res.name
        return None

class OrderInfoCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderInfoViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoSerializer
    create_serializer_class = OrderInfoCreateUpdateSerializer
    update_serializer_class = OrderInfoCreateUpdateSerializer
    filter_fields = ['user_id', 'order_no', 'transaction_id', 'status', 'is_pay', 'payment_way']
    search_fields = ['user_id', 'order_no', 'transaction_id', 'status', 'is_pay', 'payment_way']