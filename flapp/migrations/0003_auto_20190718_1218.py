# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-18 12:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flapp', '0002_auto_20190718_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='active',
            name='bend_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='报名截止时间'),
        ),
        migrations.AddField(
            model_name='active',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否活跃'),
        ),
        migrations.AddField(
            model_name='active',
            name='is_status',
            field=models.BooleanField(default=False, verbose_name='是否置顶'),
        ),
        migrations.AddField(
            model_name='voteactive',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否活跃'),
        ),
        migrations.AlterField(
            model_name='active',
            name='end_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='活动结束时间'),
        ),
    ]