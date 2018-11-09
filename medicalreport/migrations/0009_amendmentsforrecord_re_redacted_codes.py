# Generated by Django 2.1 on 2018-11-08 11:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicalreport', '0008_nhs_sensitive_conditions'),
    ]

    operations = [
        migrations.AddField(
            model_name='amendmentsforrecord',
            name='re_redacted_codes',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]