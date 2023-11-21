#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 15:49
# @Author  : harry
import datetime
import json
import re
import time

from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conf.env import DATABASE_USER, DATABASE_NAME
from user_center.models import User
from user_center.views.user import MemberSerializer
from dvadmin.utils.json_response import DetailResponse
from django.db import connection
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate

from dvadmin.utils.string_util import format_bytes

class DataVViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = MemberSerializer
    extra_filter_backends = []
    ordering_fields = ['create_time']

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def users_total(self, request):
        """
        用户总数
        :param request:
        :return:
        """
        users_total = User.objects.all().count()
        return DetailResponse(data={"users_total": users_total, }, msg="获取成功")


    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def registered_user(self, request):
        """
        用户注册趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        users = User.objects.filter(create_time__gte=seven_days_ago).annotate(
            day=TruncDay('create_time')).values(
            'day').annotate(count=Count('id')).order_by('-day')
        result = []
        data_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in users}
        for i in range(day):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({'day': date, 'count': data_dict[date] if date in data_dict else 0})
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"registered_user_list": result}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def login_user(self, request):
        """
        用户登录趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        users = User.objects.filter(update_time__gte=seven_days_ago).annotate(day=TruncDay('update_time')).values('day').annotate(count=Count('id')).order_by('-day')
        result = []
        data_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in users}
        for i in range(day):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({'day': date, 'count': data_dict[date] if date in data_dict else 0})
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"login_user": result}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def activite_user(self, request):
        """
        用户活动趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        register_users = User.objects.filter(create_time__gte=seven_days_ago).annotate(day=TruncDay('create_time')).values('day').annotate(count=Count('id')).order_by('-day')
        login_users = User.objects.filter(update_time__gte=seven_days_ago).annotate(day=TruncDay('update_time')).values('day').annotate(count=Count('id')).order_by('-day')
        result = []
        register_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in register_users}
        login_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in login_users}
        for i in range(day):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({'day': date, 'register': register_dict[date] if date in register_dict else 0, 'login': login_dict[date] if date in login_dict else 0,})
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data=result, msg="获取成功")