# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-18 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flapp', '0005_auto_20190718_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='info/', verbose_name='图片'),
        ),
    ]
