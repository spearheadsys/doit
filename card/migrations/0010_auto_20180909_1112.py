# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-09-09 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0009_auto_20180714_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_reminder', to='card.Card'),
        ),
    ]
