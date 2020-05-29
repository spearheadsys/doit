# Generated by Django 2.0 on 2019-12-22 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0019_auto_20191123_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='card_column', to='card.Column'),
        ),
        migrations.AlterField(
            model_name='card',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.Organization'),
        ),
        migrations.AlterField(
            model_name='card',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='card',
            name='priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='card.Priority'),
        ),
        migrations.AlterField(
            model_name='card',
            name='type',
            field=models.CharField(blank=True, choices=[('SR', 'Service Request'), ('IN', 'Incident')], default='SR', max_length=2),
        ),
    ]