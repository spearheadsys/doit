# Generated by Django 3.0.6 on 2020-10-28 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_delete_task'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reminder',
        ),
    ]
