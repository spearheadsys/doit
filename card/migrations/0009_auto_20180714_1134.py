# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-07-14 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_auto_20180709_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board_column', to='board.Board'),
        ),
    ]
