# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-20 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flapp', '0009_sponsor_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sanp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='active',
            name='sanp_num',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='sanp',
            name='active',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flapp.Active', verbose_name='报名活动'),
        ),
        migrations.AddField(
            model_name='sanp',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flapp.User', verbose_name='用户'),
        ),
    ]