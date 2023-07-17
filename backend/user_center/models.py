from django.db import models

# Create your models here.
class User(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delete_time = models.DateTimeField(auto_now=True)
    del_state = models.BooleanField(default=False)
    parent_id = models.BigIntegerField(default=0)
    mobile = models.CharField(max_length=11, null=True, blank=True, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, default='')
    sex = models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0)
    avatar = models.CharField(max_length=255, default='')
    info = models.CharField(max_length=255, default='')
    level = models.PositiveSmallIntegerField(default=1)
    expire_time = models.DateTimeField()
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