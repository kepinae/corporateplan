# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('address', models.TextField(max_length=400)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_req_in_plan', models.IntegerField()),
                ('free_kms_in_plan', models.IntegerField()),
                ('validity_in_months', models.IntegerField()),
                ('no_of_req_remaining', models.IntegerField()),
                ('kms_remaining', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('last_updated', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corporatePlans.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='plan_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corporatePlans.Type'),
        ),
    ]
