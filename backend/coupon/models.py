from django.db import models
from order.models import OrderGoods

from dvadmin.utils.models import CoreModel

# Create your models here.

class CouponsModel(CoreModel):
    name = models.CharField(max_length=255, verbose_name="名称")
    type = models.CharField(max_length=255, verbose_name="优惠券类型")
    value = models.FloatField(verbose_name="金额/比例")
    min_amount = models.FloatField(verbose_name="最低使用金额")
    expire_type = models.CharField(max_length=255, verbose_name="有效期类型")
    days = models.IntegerField(verbose_name="有效期")
    start_time = models.DateField(verbose_name="开始时间")
    end_time = models.DateField(verbose_name="结束时间")
    total_count = models.IntegerField(verbose_name="总数")
    claimed_count = models.IntegerField(default=0, verbose_name="领取数量")
    used_count = models.IntegerField(default=0, verbose_name="使用数量")
    status = models.SmallIntegerField(default=0, verbose_name="状态")

    class Meta:
        db_table = "coupons"
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class CouponScenesModel(CoreModel):
    coupon_id = models.IntegerField(verbose_name="优惠券ID")
    
    goods_id = models.IntegerField(verbose_name="商品ID")
    agent_id = models.IntegerField(verbose_name="代理ID")
    status = models.SmallIntegerField(default=0, verbose_name="状态")
    class Meta:
        db_table = "coupon_scenes"
        verbose_name = '使用场景'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)