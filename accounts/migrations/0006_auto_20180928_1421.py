# Generated by Django 2.1 on 2018-09-28 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20180831_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalpracticeuser',
            name='role',
            field=models.IntegerField(blank=True, choices=[(0, 'Manager'), (1, 'GP'), (2, 'SARS')], null=True, verbose_name='Role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email'),
        ),
    ]