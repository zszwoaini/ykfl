# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-20 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flapp', '0008_auto_20190718_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='spon/', verbose_name='组织图徽'),
        ),
    ]
