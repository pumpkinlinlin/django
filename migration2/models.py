from django.db import models

# Create your models here.

class User(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
        ('others', '其他'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name='用戶名') #unique表示註冊的名字不可重複
    password = models.CharField(max_length=256, verbose_name='密碼')
    email = models.EmailField(unique=True, verbose_name='信箱')
    sex = models.CharField(choices=gender, max_length=32, default='男', verbose_name='性別')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time'] #表示越晚註冊的排序越上面
        verbose_name = '用戶'
        verbose_name_plural = '用戶'

class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name='確認碼')
    user = models.OneToOneField('User', verbose_name='相對的用戶')

    c_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    def __str__(self):
        return self.user.name + "： " +self.code

    class Meta:
        ordering = ['-c_time'] #表示越晚註冊的排序越上面
        verbose_name = '確認碼'
        verbose_name_plural = '確認碼'