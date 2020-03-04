# Generated by Django 2.1 on 2018-11-21 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisations', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[('', '----'), (0, 'Manager'), (1, 'GP'), (2, 'Other practice staff')], null=True, verbose_name='Role')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.OrganisationGeneralPractice')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='instructionpermission',
            unique_together={('role', 'organisation', 'group')},
        ),
    ]