# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-03 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_card_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
