# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-10-27 19:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0011_card_sla_lifetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='sla_lifetime',
        ),
    ]
