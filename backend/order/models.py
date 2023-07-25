from django.db import models

from dvadmin.utils.models import CoreModel

class OrderInfo(CoreModel):
    del_flag = models.CharField(max_length=1, default='0')
    remark = models.CharField(max_length=500, default='')
    user_id = models.IntegerField()
    order_no = models.CharField(max_length=64, unique=True)
    payment_way = models.CharField(max_length=64)
    is_pay = models.CharField(max_length=2)
    status = models.CharField(max_length=32, default='1')
    freight_price = models.FloatField(default='0')
    sales_price = models.FloatField(default='0')
    payment_price = models.FloatField(default='0')
    payment_time = models.DateTimeField(null=True)
    delivery_time = models.DateTimeField(null=True)
    receiver_time = models.DateTimeField(null=True)
    closing_time = models.DateTimeField(null=True)
    user_message = models.CharField(max_length=255, null=True)
    transaction_id = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'order_info'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class OrderItem(CoreModel):
    del_flag = models.CharField(max_length=1, default='0')
    remark = models.CharField(max_length=500, default='')
    spu_id = models.CharField(max_length=36, null=True)
    spu_name = models.CharField(max_length=255, null=True)
    pic = models.CharField(max_length=255, null=True)
    num = models.BigIntegerField(default='1')
    sales_price = models.FloatField()
    freight_price = models.FloatField(default='0')
    payment_price = models.FloatField(default='0')
    status = models.CharField(max_length=32, default='0')
    is_refund = models.CharField(max_length=2, default='N')
    order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_item'
        verbose_name = '子订单类目'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class OrderGoods(CoreModel):
    del_flag = models.CharField(max_length=1, default='0')
    remark = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    year_num = models.IntegerField(default=0)
    month_num = models.IntegerField(default=0)
    day_num = models.IntegerField(default=0)
    sales_price = models.FloatField()
    payment_price = models.FloatField()
    sale_num = models.BigIntegerField(default='0')

    class Meta:
        db_table = 'order_goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)