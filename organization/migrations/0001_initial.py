# Generated by Django 3.0.6 on 2020-05-30 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('billing_address', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_zip_code', models.CharField(blank=True, max_length=24, null=True)),
                ('billing_city', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_country', models.CharField(blank=True, max_length=255, null=True)),
                ('bank', models.CharField(blank=True, max_length=255, null=True)),
                ('iban', models.CharField(blank=True, max_length=64, null=True)),
                ('registration_code', models.CharField(blank=True, max_length=128, null=True)),
                ('vat_number', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_time', models.DateField(auto_now=True)),
                ('modified_time', models.DateField(auto_now_add=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, upload_to='logos')),
                ('csat_exclude', models.BooleanField(default=False)),
                ('included_hours', models.IntegerField(blank=True, null=True)),
                ('sla_name', models.CharField(blank=True, max_length=255, null=True)),
                ('sla_response_time', models.IntegerField(blank=True, null=True)),
                ('allow_external_contacts', models.BooleanField(default=False)),
                ('allow_auto_contact_creation', models.BooleanField(default=False)),
                ('boards', models.ManyToManyField(related_name='organization_boards', to='board.Board')),
                ('contacts', models.ManyToManyField(blank=True, related_name='organization_contacts', to=settings.AUTH_USER_MODEL)),
                ('default_board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.Board')),
                ('email_domains', models.ManyToManyField(blank=True, related_name='email_domain', to='organization.EmailDomain')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
