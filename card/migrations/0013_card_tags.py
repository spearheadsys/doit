# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-10 06:58
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('card', '0012_remove_card_sla_lifetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
