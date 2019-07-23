# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-19 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('migration2', '0002_auto_20190716_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='確認碼')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='migration2.User', verbose_name='相對的用戶')),
            ],
            options={
                'verbose_name': '確認碼',
                'verbose_name_plural': '確認碼',
                'ordering': ['-c_time'],
            },
        ),
    ]