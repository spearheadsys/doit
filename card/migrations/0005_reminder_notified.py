# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-07 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
