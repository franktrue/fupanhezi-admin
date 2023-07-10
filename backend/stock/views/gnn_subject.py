from rest_framework import serializers
from stock.models import StockGnnSubject
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from dvadmin.utils.json_response import SuccessResponse
from stock.services.gnn_subject import StockGnnSubjectService

class StockGnnSubjectSerializer(CustomModelSerializer):
    """
    序列化器
    """
    hasChild = serializers.SerializerMethodField()

    def get_hasChild(self, instance):
        hasChild = StockGnnSubject.objects.filter(parent=instance.id)
        if hasChild:
            return True
        return False
    
    class Meta:
        model = StockGnnSubject
        fields = '__all__'
        read_only_fields = ["id"]

class StockGnnSubjectCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    name = serializers.CharField(required=False)

    class Meta:
        model = StockGnnSubject
        fields = '__all__'
        read_only_fields = ["id"]

class StockGnnSubjectInitSerializer(CustomModelSerializer):
    """
    递归深度获取数信息(用于生成初始化json文件)
    """
    name = serializers.CharField(required=False)
    children = serializers.SerializerMethodField()

    def get_children(self, obj: StockGnnSubject):
        data = []
        instance = StockGnnSubject.objects.filter(parent_id=obj.id)
        if instance:
            serializer = StockGnnSubjectInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get('children')
        menu_button = self.initial_data.get('menu_button')
        # 菜单表
        if children:
            for menu_data in children:
                menu_data['parent'] = instance.id
                filter_data = {
                    "name": menu_data['name'],
                    "web_path": menu_data['web_path'],
                    "component": menu_data['component'],
                    "component_name": menu_data['component_name'],
                }
                instance_obj = Menu.objects.filter(**filter_data).first()
                if instance_obj and not self.initial_data.get('reset'):
                    continue
                serializer = MenuInitSerializer(instance_obj, data=menu_data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return instance

    class StockGnnSubject:
        model = StockGnnSubject
        fields = ['name', 'code', 'change_pe', 'level', 'desc', 'parent', 'children']
        read_only_fields = ['id', 'children']

class StockGnnSubjectViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = StockGnnSubject.objects.all()
    serializer_class = StockGnnSubjectSerializer
    create_serializer_class = StockGnnSubjectCreateUpdateSerializer
    update_serializer_class = StockGnnSubjectCreateUpdateSerializer
    search_fields = ['code', 'name']
    filter_fields = ['code', 'name']

    def list(self,request):
        """懒加载"""
        params = request.query_params
        parent = params.get('parent', None)
        if params:
            if parent:
                queryset = self.queryset.filter(parent=parent)
            else:
                queryset = self.queryset
        else:
            queryset = self.queryset.filter(parent__isnull=True)
        queryset = self.filter_queryset(queryset)
        serializer = StockGnnSubjectSerializer(queryset, many=True, request=request)
        data = serializer.data
        return SuccessResponse(data=data)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def fetch(self, request):
        service = StockGnnSubjectService()
        service.fetch()
        return SuccessResponse(data=[], msg="同步成功")