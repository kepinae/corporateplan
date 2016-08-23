# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 11:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('corporatePlans', '0002_auto_20160819_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='Uid',
        ),
        migrations.AddField(
            model_name='company',
            name='UID',
            field=models.CharField(default=datetime.datetime(2016, 8, 19, 11, 7, 38, 433221, tzinfo=utc), max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
