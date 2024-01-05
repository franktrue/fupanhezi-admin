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
    claimed_count = models.IntegerField(default=0, verbose_name="领取数量")
    used_count = models.IntegerField(default=0, verbose_name="使用数量")
    status = models.SmallIntegerField(default=0, verbose_name="状态")
    class Meta:
        db_table = "coupon_scenes"
        verbose_name = '使用场景'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class CouponExchangesModel(CoreModel):
    del_flag = models.BooleanField(max_length=1, default=0)
    name = models.CharField(max_length=255, null=True)
    year_num = models.IntegerField(default=0)
    month_num = models.IntegerField(default=0)
    day_num = models.IntegerField(default=0)
    used_count = models.BigIntegerField(default=0)
    level = models.SmallIntegerField(default=1, verbose_name="对应等级")
    expire_type = models.CharField(max_length=255, verbose_name="有效期类型")
    days = models.IntegerField(verbose_name="有效期")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    class Meta:
        db_table = "coupon_exchanges"
        verbose_name = '兑换码场景'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class CouponExchangeCodesModel(CoreModel):
    del_flag = models.BooleanField(max_length=1, default=False)
    key = models.CharField(max_length=16, unique=True, verbose_name="兑换码")
    exchange_id = models.IntegerField(verbose_name="兑换码场景ID")
    user_id = models.IntegerField(default=0, verbose_name="用户ID")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    status = models.BooleanField(max_length=1, default=0)
    class Meta:
        db_table = "coupon_exchange_codes"
        verbose_name = '兑换码'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)