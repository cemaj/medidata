# Generated by Django 2.1 on 2018-11-21 07:40

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisations', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('type', models.CharField(choices=[('MEDI', 'Medidata'), ('CLT', 'Client'), ('GP', 'General Practice'), ('PAT', 'Patient')], max_length=4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GpPractices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=255)),
                ('comm_area', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('billing_address_street1', models.CharField(max_length=255)),
                ('billing_address_street2', models.CharField(max_length=255, null=True)),
                ('billing_address_street3', models.CharField(max_length=255, null=True)),
                ('billing_address_street', models.CharField(max_length=255)),
                ('billing_address_city', models.CharField(max_length=255)),
                ('billing_address_state', models.CharField(max_length=255)),
                ('billing_address_postalcode', models.CharField(max_length=255)),
                ('phone_office', models.CharField(max_length=255)),
                ('phone_alternate', models.CharField(max_length=255, null=True)),
                ('respcode_c', models.CharField(max_length=255)),
                ('salutation', models.CharField(max_length=255)),
                ('initials', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('practicemanagername_c', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('patientlistsize_c', models.CharField(max_length=255)),
                ('urn_c', models.CharField(max_length=255)),
                ('sitenumber_c', models.CharField(max_length=255)),
                ('employees', models.CharField(max_length=255)),
                ('ownership', models.CharField(max_length=255)),
                ('ccg_health_board_c', models.CharField(max_length=255)),
                ('sic_code', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('greeting', models.CharField(max_length=255)),
                ('email1', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(choices=[('', '----'), ('DR', 'Dr.'), ('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Ms.'), ('MX', 'Mx.')], max_length=3)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('maiden_name', models.CharField(blank=True, max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address_name_number', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('address_line3', models.CharField(blank=True, max_length=255)),
                ('address_postcode', models.CharField(blank=True, max_length=255)),
                ('address_country', models.CharField(blank=True, max_length=255)),
                ('telephone_home', models.CharField(blank=True, max_length=255)),
                ('telephone_mobile', models.CharField(blank=True, max_length=255)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
            ],
            options={
                'verbose_name': 'User Profile Base',
                'verbose_name_plural': 'User Profile Bases',
            },
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.UserProfileBase')),
                ('role', models.IntegerField(blank=True, choices=[(0, 'Client Admin'), (1, 'Client')], null=True, verbose_name='Role')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.OrganisationClient')),
            ],
            options={
                'verbose_name': 'Client User',
            },
            bases=('accounts.userprofilebase',),
        ),
        migrations.CreateModel(
            name='GeneralPracticeUser',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.UserProfileBase')),
                ('role', models.IntegerField(blank=True, choices=[('', '----'), (0, 'Manager'), (1, 'GP'), (2, 'Other practice staff')], null=True, verbose_name='Role')),
                ('code', models.CharField(blank=True, max_length=255)),
                ('payment_bank_holder_name', models.CharField(blank=True, max_length=255)),
                ('payment_bank_account_number', models.CharField(blank=True, max_length=255)),
                ('payment_bank_sort_code', models.CharField(blank=True, max_length=255)),
                ('can_complete_amra', models.BooleanField(default=False)),
                ('can_complete_sars', models.BooleanField(default=False)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.OrganisationGeneralPractice')),
            ],
            options={
                'verbose_name': 'General Practice User',
            },
            bases=('accounts.userprofilebase',),
        ),
        migrations.CreateModel(
            name='MedidataUser',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.UserProfileBase')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.OrganisationMedidata')),
            ],
            options={
                'verbose_name': 'Medidata User',
            },
            bases=('accounts.userprofilebase',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('userprofilebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.UserProfileBase')),
                ('nhs_number', models.CharField(blank=True, max_length=10)),
                ('emis_number', models.CharField(blank=True, max_length=255)),
                ('vision_number', models.CharField(blank=True, max_length=255)),
                ('systmone_number', models.CharField(blank=True, max_length=255)),
                ('microtest_number', models.CharField(blank=True, max_length=255)),
                ('patient_input_email', models.EmailField(blank=True, max_length=255)),
                ('alternate_phone', models.CharField(blank=True, max_length=255)),
                ('organisation_gp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.OrganisationGeneralPractice')),
            ],
            options={
                'verbose_name': 'Patient User',
            },
            bases=('accounts.userprofilebase',),
        ),
        migrations.AddField(
            model_name='userprofilebase',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
