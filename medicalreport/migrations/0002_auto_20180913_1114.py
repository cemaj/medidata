# Generated by Django 2.1 on 2018-09-13 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicalreport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalmedicationrecords',
            name='snomed_concept',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='snomedct.SnomedConcept'),
        ),
    ]
