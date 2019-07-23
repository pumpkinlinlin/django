# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-15 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='用戶名')),
                ('password', models.CharField(max_length=256, verbose_name='密碼')),
                ('email', models.CharField(choices=[('male', '男'), ('female', '女'), ('others', '其他')], default='男', max_length=32, verbose_name='信箱')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
            ],
            options={
                'verbose_name': '用戶',
                'verbose_name_plural': '用戶',
                'ordering': ['-c_time'],
            },
        ),
    ]