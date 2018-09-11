# Generated by Django 2.1 on 2018-09-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReadCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_read_code', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('file_path', models.CharField(max_length=255)),
                ('concept_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SnomedConcept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.BigIntegerField(unique=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('file_path', models.CharField(max_length=255)),
                ('fsn_description', models.CharField(max_length=255)),
                ('external_fsn_description_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SnomedDescendant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.BigIntegerField()),
                ('descendant_external_id', models.BigIntegerField()),
            ],
        ),
    ]
