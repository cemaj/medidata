# Generated by Django 2.1 on 2018-10-17 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalreport', '0002_auto_20181016_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='amendmentsforrecord',
            name='instruction_checked',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
