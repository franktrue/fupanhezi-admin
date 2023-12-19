from user_center.models import UserAgent
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.json_response import DetailResponse
from stock.utils.cache import delete_cache_by_key

class UserAgentSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = UserAgent
        fields = '__all__'

class UserAgentCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = UserAgent
        fields = '__all__'

class UserAgentViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = UserAgent.objects.all()
    serializer_class = UserAgentSerializer
    create_serializer_class = UserAgentCreateUpdateSerializer
    update_serializer_class = UserAgentCreateUpdateSerializer
    filter_fields = ['agent_id', 'reward_type', 'status']
    cache_key = "cache:fupanhezi:userAgent:id:"

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