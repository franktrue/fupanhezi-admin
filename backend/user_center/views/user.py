# -*- coding: utf-8 -*-
from django.db.models import Sum
from rest_framework import serializers
from user_center.models import User, UserReward, UserWithdrawRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from stock.utils.cache import delete_cache_by_key
from user_center.services.qrocde import QrcodeService

class MemberSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = User
        fields = '__all__'

    has_children = serializers.SerializerMethodField()

    reward_amount = serializers.SerializerMethodField()
    withdraw_amount = serializers.SerializerMethodField()

    reward_info = serializers.SerializerMethodField()

    def get_has_children(self, obj: User):
        return User.objects.filter(parent_id=obj.id).count()
    
    # 佣金总金额
    def get_reward_amount(self, obj: User):
        res = UserReward.objects.filter(user_id=obj.id).aggregate(Sum("amount"))
        return res['amount__sum']
    
    # 已提现金额
    def get_withdraw_amount(self, obj: User):
        res = UserWithdrawRecord.objects.filter(user_id=obj.id, status='2').aggregate(Sum("amount"))
        return res['amount__sum']
    
    def get_reward_info(self, obj: User):
        if obj.reward_type == 'percent':
            return f"百分比：{obj.reward_value}%"
        return f"固额：{obj.reward_value}元"

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
    filter_fields = ['id', 'parent_id', 'nickname', 'mobile', 'is_agent']
    cache_key = "cache:fupanhezi:user:id:"

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
    
    # 获取小程序码
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def qrcode(self, request, *args, **kwargs):
        scene = request.data.get('scene')
        page = request.data.get('page')
        service = QrcodeService()
        data = service.unlimited(scene = scene, page = page)
        return DetailResponse(data=data, msg="成功")
