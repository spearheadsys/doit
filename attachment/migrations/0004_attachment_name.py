# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-29 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachment', '0003_auto_20180909_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
