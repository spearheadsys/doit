# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-03 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_oncall',
            field=models.BooleanField(default=True),
        ),
    ]
