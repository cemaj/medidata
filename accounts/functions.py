from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from .forms import NewGPForm, NewClientForm
from .tables import UserTable
from .models import User, GENERAL_PRACTICE_USER, CLIENT_USER, MEDIDATA_USER, PATIENT_USER,\
        Patient, GeneralPracticeUser, ClientUser, UserProfileBase

DEFAULT_FROM = settings.DEFAULT_FROM


def reset_password(request):
    emails = request.POST.getlist("users[]")
    PASSWORD = 'medi2018'
    user_cnt = len(emails)
    organisations = set()
    for email in emails:
        user = User.objects.get(email=email)
        if user.type == GENERAL_PRACTICE_USER and hasattr(user, 'userprofilebase') and\
            hasattr(user.userprofilebase, 'generalpracticeuser') and\
            user.userprofilebase.generalpracticeuser.organisation:
            organisations.add(user.userprofilebase.generalpracticeuser.organisation.organisation_email)
        user.set_password(PASSWORD)
        user.save()
        # send_mail(
        #     'Your account password has been changed',
        #     'Your account password has been changed by your manager. Password: {}'.format(PASSWORD),
        #     DEFAULT_FROM,
        #     [user.email],
        #     fail_silently=True,
        #     auth_user=get_env_variable('SENDGRID_USER'),
        #     auth_password=get_env_variable('SENDGRID_PASS'),
        # )

    for organisation_email in organisations:
        send_mail(
            'Reset password',
            'User password has been changed by your manager.',
            DEFAULT_FROM,
            [organisation_email],
            fail_silently=True,
        )

    if user_cnt == 1:
        messages.success(request, "The selected user's password has been reset. Password: {}".format(PASSWORD))
    else:
        messages.success(request, "All the passwords of the selected users have been reset. Password: {}".format(PASSWORD))


def change_role(request):
    cur_user = request.user
    cur_user = User.objects.get(username=cur_user.username)
    role = request.POST.get("role")
    emails = request.POST.getlist("users[]")
    user_cnt = len(emails)
    for email in emails:
        user = User.objects.get(email=email)
        if role == 0:
            user.is_staff = True
        else:
            user.is_staff = False
        user.save()

        if hasattr(cur_user.userprofilebase, 'generalpracticeuser'):
            user.userprofilebase.generalpracticeuser.role = role
            user.userprofilebase.generalpracticeuser.save()
        elif hasattr(cur_user.userprofilebase, 'clientuser'):
            user.userprofilebase.clientuser.role = role
            user.userprofilebase.clientuser.save()

    if user_cnt == 1:
        messages.success(request, "The role of selected user has been changed.")
    else:
        messages.success(request, "All the roles of the selected users have been changed.")


def remove_user(request):
    emails = request.POST.getlist("users[]")
    user_cnt = len(emails)
    for email in emails:
        user = User.objects.get(email=email)
        user.userprofilebase.delete()

    if user_cnt == 1:
        messages.success(request, "The selected user has been deleted.")
    else:
        messages.success(request, "Selected users have been deleted.")


def count_gpusers(queryset):
    all_count = queryset.count()
    pmanager_count = queryset.filter(userprofilebase__generalpracticeuser__role=0).count()
    gp_count = queryset.filter(userprofilebase__generalpracticeuser__role=1).count()
    sars_count = queryset.filter(userprofilebase__generalpracticeuser__role=2).count()
    overall_users_number = {
        'All': all_count,
        'Manager': pmanager_count,
        'GP': gp_count,
        'SARS': sars_count
    }
    return overall_users_number


def count_clientusers(queryset):
    all_count = queryset.count()
    admin_count = queryset.filter(userprofilebase__clientuser__role=0).count()
    client_count = queryset.filter(userprofilebase__clientuser__role=1).count()
    overall_users_number = {
        'All': all_count,
        'Admin': admin_count,
        'Client': client_count
    }
    return overall_users_number


def count_users(queryset):
    all_count = queryset.count()
    admin_count = queryset.filter(userprofilebase__clientuser__role=0).count()
    client_count = queryset.filter(userprofilebase__clientuser__role=1).count()
    pmanager_count = queryset.filter(userprofilebase__generalpracticeuser__role=0).count()
    gp_count = queryset.filter(userprofilebase__generalpracticeuser__role=1).count()
    sars_count = queryset.filter(userprofilebase__generalpracticeuser__role=2).count()
    medi_count = queryset.filter(type=MEDIDATA_USER).count()
    overall_users_number = {
        'All': all_count,
        'Admin': admin_count,
        'Client': client_count,
        'Manager': pmanager_count,
        'GP': gp_count,
        'SARS': sars_count,
        'Medidata': medi_count
    }
    return overall_users_number


def get_table_data(user, query_set, filter_query):
    if hasattr(user.userprofilebase, 'generalpracticeuser'):
        return {
            "user_type": "gp",
            "overall_users_number": count_gpusers(query_set),
            "table": UserTable(filter_query)
        }
    elif hasattr(user.userprofilebase, 'clientuser'):
        return {
            "user_type": "client",
            "overall_users_number": count_clientusers(query_set),
            "table": UserTable(filter_query)
        }
    elif hasattr(user.userprofilebase, 'medidatauser'):
        return {
            "user_type": "medidata",
            "overall_users_number": count_users(query_set),
            "table": UserTable(filter_query)
        }


def get_post_new_user_data(cur_user, request, user_role):
    if hasattr(cur_user.userprofilebase, 'generalpracticeuser'):
        return {
            "organisation": cur_user.userprofilebase.generalpracticeuser.organisation,
            "newuser_form": NewGPForm(request.POST),
            "user_type": GENERAL_PRACTICE_USER,
            "is_staff": True if user_role == '0' else False
        }
    elif hasattr(cur_user.userprofilebase, 'clientuser'):
        return {
            "organisation": cur_user.userprofilebase.clientuser.organisation,
            "newuser_form": NewClientForm(request.POST),
            "user_type": CLIENT_USER,
            "is_staff": True if user_role == '0' else False
        }


def get_user_type_form(cur_user):
    if hasattr(cur_user.userprofilebase, 'generalpracticeuser'):
        return {
            "newuser_form": NewGPForm(),
            "user_type": "gp"
        }
    elif hasattr(cur_user.userprofilebase, 'clientuser'):
        return {
            "newuser_form": NewClientForm(),
            "user_type": "client"
        }


def create_or_update_patient_user(patient_information, patient_emis_number) -> Patient:
    password = User.objects.make_random_password()
    patient = Patient.objects.filter(emis_number=patient_emis_number).first()

    if patient:
        patient.nhs_number = patient_information.patient_nhs_number
        patient.address_name_number = patient_information.patient_address_number
        patient.title = patient_information.patient_title
        patient.address_postcode = patient_information.patient_postcode
        patient.date_of_birth = patient_information.patient_dob
        patient.save()

        user = patient.user
        if not User.objects.filter(email=patient_information.patient_email).exists():
            user.email = patient_information.patient_email
        user.first_name = patient_information.patient_first_name
        user.last_name = patient_information.patient_last_name
        user.save()
    else:
        if patient_information.patient_email and not User.objects.filter(email=patient_information.patient_email).exists():
            user = User.objects._create_user(
                email=patient_information.patient_email,
                username=patient_emis_number,
                password=password,
                first_name=patient_information.patient_first_name,
                last_name=patient_information.patient_last_name,
                type=PATIENT_USER,
            )

            patient = Patient.objects.create(
                user=user,
                address_name_number=patient_information.patient_address_number,
                nhs_number=patient_information.patient_nhs_number,
                emis_number=patient_emis_number,
                date_of_birth=patient_information.patient_dob,
                address_postcode=patient_information.patient_postcode,
                title=patient_information.patient_title
            )

    return patient


def notify_admins(func):
    def wrapper(request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        to_emails = []
        profiles = UserProfileBase.all_objects.all()
        if hasattr(user, 'userprofilebase'):
            if hasattr(user.userprofilebase, 'clientuser'):
                organisation = user.userprofilebase.clientuser.organisation
                to_emails = [ client.email for client in User.objects.filter(
                    userprofilebase__in=profiles.alive(),
                    userprofilebase__clientuser__organisation=organisation,
                    userprofilebase__clientuser__role=ClientUser.CLIENT_ADMIN)
                ]
            elif hasattr(user.userprofilebase, 'generalpracticeuser'):
                organisation = user.userprofilebase.generalpracticeuser.organisation
                to_emails = [ client.email for client in User.objects.filter(
                    userprofilebase__in=profiles.alive(),
                    userprofilebase__generalpracticeuser__organisation=organisation,
                    userprofilebase__generalpracticeuser__role=GeneralPracticeUser.PRACTICE_MANAGER)
                ]
        if to_emails:
            send_mail(
                'Change password',
                'FYI %s has reset their password'%user.get_full_name(),
                'MediData',
                to_emails,
                fail_silently=True,
            )
        return func(request, *args, **kwargs)
    return wrapper
