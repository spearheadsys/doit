# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 13:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_board_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
