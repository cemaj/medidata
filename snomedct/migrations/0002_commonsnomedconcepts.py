# Generated by Django 2.1 on 2018-09-16 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snomedct', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonSnomedConcepts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snomed_concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snomedct.SnomedConcept')),
            ],
        ),
    ]
