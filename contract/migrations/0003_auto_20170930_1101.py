# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-30 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0002_auto_20170917_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='sla',
            name='repair_time',
            field=models.IntegerField(default=480),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sla',
            name='response_time',
            field=models.IntegerField(default=240),
            preserve_default=False,
        ),
    ]
