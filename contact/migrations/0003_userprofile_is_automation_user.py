# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-04 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_userprofile_is_oncall'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_automation_user',
            field=models.BooleanField(default=False),
        ),
    ]
