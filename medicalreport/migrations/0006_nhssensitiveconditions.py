# Generated by Django 2.1 on 2018-11-07 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalreport', '0005_remove_amendmentsforrecord_patient_emis_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='NhsSensitiveConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.IntegerField()),
                ('snome_code', models.IntegerField()),
            ],
        ),
    ]