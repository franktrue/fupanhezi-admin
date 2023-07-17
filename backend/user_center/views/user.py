from user_center.models import User
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet

class MemberSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = User
        fields = '__all__'

class MemberCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = User
        fields = '__all__'

class UserViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = User.objects.all()
    serializer_class = MemberSerializer
    create_serializer_class = MemberCreateUpdateSerializer
    update_serializer_class = MemberCreateUpdateSerializer
    filter_fields = ['parent_id', 'nickname', 'mobile']
