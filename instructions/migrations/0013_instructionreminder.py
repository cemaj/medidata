# Generated by Django 2.1 on 2018-12-20 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0012_merge_20181219_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('reminder_day', models.IntegerField()),
                ('instruction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reminders', to='instructions.Instruction')),
            ],
            options={
                'verbose_name': 'Instruction Reminder',
            },
        ),
    ]
