from django.db import models
from order.models import OrderInfo
from dvadmin.utils.models import CoreModel

# Create your models here.
class User(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(auto_now=True)
    del_state = models.BooleanField(default=False)
    parent_id = models.BigIntegerField(default=0)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, default='')
    sex = models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    info = models.CharField(max_length=255, null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=1)

    reward_type = models.CharField(max_length=30, null=False, default="percent")
    reward_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    expire_time = models.DateTimeField()
    is_agent = models.SmallIntegerField(default=0, verbose_name="是否代理")
    reward1 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="一级分佣比例")
    reward2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="二级分佣比例")
    reward3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="三级分佣比例")

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

class UserAuth(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(auto_now=True)
    del_state = models.BooleanField(default=False)
    user_id = models.PositiveIntegerField(default=1)
    auth_key = models.CharField(max_length=255)
    auth_type = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'user_auth'
        verbose_name = '第三方登录'
        verbose_name_plural = verbose_name
        unique_together = (('user_id', 'auth_type'), ('auth_type', 'auth_key'))

class UserWithdrawRecord(CoreModel):
    user_id = models.IntegerField(null=False)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    status = models.CharField(max_length=2, null=False, default="0")
    transaction_id = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=32)

    class Meta:
        db_table = 'user_withdraw_record'
        verbose_name = '提现记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class UserReward(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(auto_now=True)
    del_state = models.BooleanField(default=False)

    user = models.ForeignKey(
        to="User",
        verbose_name="所属用户",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="所属用户",
    )
    invite_user_id = models.BigIntegerField(default=0)
    order = models.ForeignKey(
        to=OrderInfo,
        verbose_name="关联订单",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联订单",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.SmallIntegerField(default=1)
    remark = models.CharField(max_length=255, null=True, default="")

    class Meta:
        db_table = 'user_reward'
        verbose_name = '奖励记录'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

class UserCoupon(models.Model):
    agent_id = models.BigIntegerField(default=0, verbose_name="代理ID")
    user_id = models.BigIntegerField(default=0, verbose_name="所属用户")
    scene_id = models.BigIntegerField(default=0, verbose_name="领取场景ID")
    claimed_time = models.DateTimeField(auto_now_add=True, verbose_name="领取时间")
    used_time = models.DateTimeField(null=True, verbose_name="使用时间")
    coupon_id = models.BigIntegerField(verbose_name="优惠券ID")
    name = models.CharField(max_length=255, verbose_name="名称")
    goods_id = models.IntegerField(default=0, verbose_name="优惠券ID")
    type = models.CharField(max_length=255, verbose_name="优惠类型")
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="优惠值")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="最小使用金额")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    status = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'user_coupons'
        verbose_name = '用户优惠券'
        verbose_name_plural = verbose_name
        ordering = ('-claimed_time',)

class UserAgent(CoreModel):
    agent_id = models.BigIntegerField(default=0, verbose_name="代理ID")
    reward_type = models.CharField(max_length=30, null=False, default="percent")
    reward1 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="一级下线分佣比例")
    reward2 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="二级下线分佣比例")
    reward3 = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="三级下线分佣比例")
    end_time = models.DateTimeField()
    status = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'user_agent'
        verbose_name = '代理设置'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)