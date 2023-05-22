from django.db import models

# Create your models here.

class StockZtHistory(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    date = models.DateField(verbose_name='日期')
    stock_code = models.CharField(max_length=10, verbose_name='股票代码')
    stock_name = models.CharField(max_length=32, verbose_name='股票名称')
    fb_amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='封板金额')
    first_zt_time = models.CharField(max_length=10, verbose_name='首次涨停时间', default='')
    last_zt_time = models.CharField(max_length=10, verbose_name='最后一次涨停时间', default='')
    zb_num = models.SmallIntegerField(verbose_name='开板次数', default=-1)
    zt_statistics = models.CharField(max_length=32, verbose_name='涨停统计情况', default='')
    ztlb_num = models.SmallIntegerField(verbose_name='连板天数', default=0)
    sort = models.FloatField(max_length=4, verbose_name='排序', default=0.0)
    z_sz = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='总市值', default=0.00)
    lt_sz = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='流通市值', default=0.00)
    zs_sz = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='自由流通市值', default=0.00)
    hs_rate = models.FloatField(max_length=10, verbose_name='换手率', default=0.00)
    real_hs_rate = models.FloatField(max_length=10, verbose_name='实际换手率', default=0.00)
    pe = models.FloatField(max_length=10, verbose_name='市盈率', default=0.00)
    zt_type = models.CharField(max_length=64, verbose_name='涨停类型', default='')
    zt_reson = models.CharField(max_length=1000, verbose_name='涨停原因', default='')

    class Meta:
        db_table = 'stock_zt_history'
        verbose_name = '涨停股历史'
        verbose_name_plural = verbose_name
        unique_together = ['date', 'stock_code']  # 添加联合唯一索引
        ordering = ('-date', '-ztlb_num', 'first_zt_time', 'zb_num',)

class StockHistory(models.Model):
    date = models.DateField(null=False)
    stock_code = models.CharField(max_length=10, null=False)
    stock_name = models.CharField(max_length=32, null=False, default='')
    open = models.FloatField(null=False)
    close = models.FloatField(null=False)
    high = models.FloatField(null=False)
    low = models.FloatField(null=False)
    pre_close = models.FloatField(null=False)
    vol = models.BigIntegerField(null=False)
    amo = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    hs_rate = models.FloatField(null=False)
    change_amo = models.FloatField(null=False)
    open_pe = models.FloatField(null=False)
    high_pe = models.FloatField(null=False)
    low_pe = models.FloatField(null=False)
    close_pe = models.FloatField(null=False)
    is_lhb = models.SmallIntegerField(null=False, default=0)
    lhb_reson = models.CharField(max_length=255, null=False, default='')
    lhb_parse = models.CharField(max_length=128, null=False, default='')

    class Meta:
        db_table = 'stock_history'
        verbose_name = '股票行情'
        verbose_name_plural = verbose_name
        unique_together = ('date', 'stock_code')
        ordering = ('-date',)

class StockTradeDate(models.Model):
    trade_date = models.DateField(null=False)

    class Meta:
        db_table = 'stock_trade_date'
        verbose_name = '交易日'
        verbose_name_plural = verbose_name
        ordering = ('-trade_date',)

class StockBoardIndustry(models.Model):
    TYPE = 'industry'

    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=64, null=False, default='')

    class Meta:
        db_table = 'stock_board_industry'
        verbose_name = '行业板块'
        verbose_name_plural = verbose_name

class StockBoardConcept(models.Model):
    TYPE = 'concept'

    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=64, null=False, default='')
    release_date = models.DateField(null=True)
    show_url = models.CharField(max_length=255, null=False, default='')
    include_number = models.IntegerField(verbose_name='成分股数量', default=0)

    class Meta:
        db_table = 'stock_board_concept'
        verbose_name = '概念板块'
        verbose_name_plural = verbose_name

class StockBoardMap(models.Model):
    code = models.CharField(max_length=10, null=False)
    board_name = models.CharField(max_length=64, null=False, default='')
    stock_code = models.CharField(max_length=10, null=False)
    stock_name = models.CharField(max_length=32, null=False, default='')
    type = models.CharField(max_length=20, null=False, default='')

    class Meta:
        db_table = 'stock_board_map'
        verbose_name = '板块成分股'
        verbose_name_plural = verbose_name
        unique_together = ('code', 'stock_code')

class StockLhb(models.Model):
    date = models.DateField(null=True)
    serial = models.SmallIntegerField(null=True)
    stock_code = models.CharField(max_length=10, null=True)
    stock_name = models.CharField(max_length=32, null=True)
    interpretation = models.CharField(max_length=256, null=True)
    close = models.FloatField(null=True)
    close_pe = models.FloatField(null=True)
    lhb_net_buy_amo = models.BigIntegerField(null=True)
    lhb_buy_amo = models.BigIntegerField(null=True)
    lhb_sell_amo = models.BigIntegerField(null=True)
    lhb_amo = models.BigIntegerField(null=True)
    market_total_amo = models.BigIntegerField(null=True)
    net_buy_amo_pe = models.BigIntegerField(null=True)
    amo_pe = models.FloatField(null=True)
    hs_rate = models.FloatField(null=True)
    circulate_market_value = models.BigIntegerField(null=True)
    rank_reson = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'stock_lhb'
        verbose_name = '龙虎榜'
        verbose_name_plural = verbose_name
        unique_together = ('date', 'stock_code')
        ordering = ('-date',)
