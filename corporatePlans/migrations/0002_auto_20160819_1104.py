# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 11:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('corporatePlans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='Uid',
            field=models.SlugField(default=datetime.datetime(2016, 8, 19, 11, 4, 34, 351310, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.SlugField(),
        ),
    ]
