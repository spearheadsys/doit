# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='priority',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
