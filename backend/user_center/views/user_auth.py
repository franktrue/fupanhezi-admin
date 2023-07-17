from user_center.models import UserAuth
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class UserAuthSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = UserAuth
        fields = '__all__'

class UserAuthCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = UserAuth
        fields = '__all__'

class UserAuthViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = UserAuth.objects.all()
    serializer_class = UserAuthSerializer
    create_serializer_class = UserAuthCreateUpdateSerializer
    update_serializer_class = UserAuthCreateUpdateSerializer
    filter_fields = ['user_id', 'auth_key', 'auth_type']
