# Generated by Django 2.1 on 2018-11-08 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_create_custom_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='alternate_phone',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
