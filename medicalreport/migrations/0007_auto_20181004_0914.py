# Generated by Django 2.1 on 2018-10-04 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalreport', '0006_auto_20181004_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalallergies',
            name='redaction',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='additionalmedicationrecords',
            name='redaction',
            field=models.IntegerField(),
        ),
    ]