# Generated by Django 2.1 on 2018-10-02 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0005_auto_20181001_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='rejected_type',
            field=models.IntegerField(blank=True, choices=[(0, 'No suitable patient can be found'), (1, 'The patient is no longer registered at this practice'), (2, 'The consent form is invalid'), (3, 'Inappropriate purpose for Subject Access Request')], null=True),
        ),
    ]