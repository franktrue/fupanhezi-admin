from user_center.models import UserWithdrawRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class UserWithdrawRecordSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = UserWithdrawRecord
        fields = '__all__'

class UserWithdrawRecordCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = UserWithdrawRecord
        fields = '__all__'

class UserWithdrawRecordViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = UserWithdrawRecord.objects.all()
    serializer_class = UserWithdrawRecordSerializer
    create_serializer_class = UserWithdrawRecordCreateUpdateSerializer
    update_serializer_class = UserWithdrawRecordCreateUpdateSerializer
    filter_fields = ['user_id', 'transaction_id', 'status', 'type']