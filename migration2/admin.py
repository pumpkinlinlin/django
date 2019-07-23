from django.contrib import admin

# Register your models here.

from . import models #.代表整個app，從app的其他部分import過來(這裡是從modelㄋ)

admin.site.register(models.User) #在admin註冊這個model
#到終端機創建superuser來管理

admin.site.register(models.ConfirmString)