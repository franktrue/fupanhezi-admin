from user_center.models import UserReward, User
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework import serializers

class UserRewardSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = UserReward
        fields = '__all__'

    user_name = serializers.CharField(read_only=True, source='user.nickname')
    order_no = serializers.CharField(read_only=True, source='order.order_no')
    invite_user = serializers.SerializerMethodField()

    def get_invite_user(self, instance):
        if instance.invite_user_id > 0 :
            return User.objects.filter(id=instance.invite_user_id).first().nickname
        return ""

class UserRewardCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = UserReward
        fields = '__all__'

class UserRewardViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = UserReward.objects.all()
    serializer_class = UserRewardSerializer
    create_serializer_class = UserRewardCreateUpdateSerializer
    update_serializer_class = UserRewardCreateUpdateSerializer
    filter_fields = ['user_id', 'invite_user_id', 'order_id']

    def get_queryset(self):
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('user', 'order')
        return queryset
