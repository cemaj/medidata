# Generated by Django 2.1 on 2018-11-23 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_auto_20181123_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationclient',
            name='companies_house_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='contact_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='contact_telephone',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='fax_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='generic_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='generic_telephone',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='organisationclient',
            name='vat_number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]