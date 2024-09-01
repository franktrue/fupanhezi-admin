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
from order.models import OrderInfo
from order.views.info import OrderInfoSerializer
from dvadmin.utils.json_response import DetailResponse
from django.db import connection
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate

from dvadmin.utils.string_util import format_bytes

class DataVViewSet(GenericViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoSerializer
    extra_filter_backends = []
    ordering_fields = ['create_time']

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def order_total(self, request):
        """
        订单总金额
        :param request:
        :return:
        """
        order_total = OrderInfo.objects.filter(is_pay = "1").exclude(status="10").aggregate(total=Sum('payment_price'))
        return DetailResponse(data={"order_total": round(order_total['total'], 2), }, msg="获取成功")



    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def order_trend(self, request):
        """
        订单金额趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        orders = OrderInfo.objects.filter(create_datetime__gte=seven_days_ago, is_pay='1').exclude(status="10").annotate(day=TruncDay('create_datetime')).values('day').annotate(amount=Sum('payment_price'), pay_count=Count('id')).order_by('-day')
        print(orders)
        result = []
        amount_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('amount') for ele in orders}
        count_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('pay_count') for ele in orders}
        for i in range(day):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({
                'day': date, 
                'amount': round(amount_dict[date], 2) if date in amount_dict else 0, 
                'pay_count': count_dict[date] if date in count_dict else 0    
            })
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"order_list": result}, msg="获取成功")
