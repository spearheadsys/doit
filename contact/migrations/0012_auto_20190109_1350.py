# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-09 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0011_auto_20190106_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_oncall',
            field=models.BooleanField(default=False),
        ),
    ]
