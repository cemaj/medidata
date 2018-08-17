# Generated by Django 2.1 on 2018-08-17 04:02

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trading_name', models.CharField(max_length=255)),
                ('legal_name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('contact_name', models.CharField(max_length=255)),
                ('contact_telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('contact_email', models.EmailField(max_length=254)),
                ('generic_telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('generic_email', models.EmailField(max_length=254)),
                ('fax_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('companies_house_number', models.CharField(max_length=255)),
                ('vat_number', models.CharField(max_length=255)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('deleted_timestamp', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='OrganizationClient',
            fields=[
                ('organizationbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='organizations.OrganizationBase')),
                ('type', models.IntegerField(choices=[(1, 'Insurance Underwriter'), (2, 'Insurance Claim'), (3, 'MediData'), (4, 'Medicolegal')])),
                ('fca_number', models.CharField(blank=True, max_length=255)),
                ('division', models.TextField(blank=True)),
                ('can_create_amra', models.BooleanField(default=False)),
                ('can_create_sars', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Organization Client',
            },
            bases=('organizations.organizationbase',),
        ),
        migrations.CreateModel(
            name='OrganizationGeneralPractice',
            fields=[
                ('organizationbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='organizations.OrganizationBase')),
                ('operating_system', models.CharField(choices=[('EW', 'EMIS-Web'), ('EP', 'EMIS-PCS'), ('EL', 'EMIS-LV'), ('ST', 'Systml'), ('VT', 'Vision Three'), ('VA', 'Vision Anywhere'), ('MT', 'Microtest'), ('OT', 'Other')], max_length=2)),
                ('operating_system_socket_endpoint', models.CharField(max_length=255)),
                ('operating_system_auth_token', models.CharField(max_length=255)),
                ('practice_code', models.CharField(max_length=255)),
                ('payment_timing', models.CharField(choices=[('AR', 'Arrears'), ('AD', 'Advance')], max_length=2)),
                ('payment_bank_holder_name', models.CharField(max_length=255)),
                ('payment_bank_sort_code', models.CharField(max_length=255)),
                ('payment_bank_account_number', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Organization GeneralPractice',
            },
            bases=('organizations.organizationbase',),
        ),
    ]
