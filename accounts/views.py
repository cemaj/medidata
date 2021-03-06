from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse
from django.forms import modelformset_factory

from permissions.forms import InstructionPermissionForm, GroupPermissionForm
from permissions.models import InstructionPermission
from common.functions import multi_getattr, verify_password as verify_pass
from payment.models import OrganisationFee
from django_tables2 import RequestConfig
from accounts.forms import AllUserForm, NewGPForm, NewClientForm, NewMediForm

from .models import User, UserProfileBase, GeneralPracticeUser, PracticePreferences
from .models import GENERAL_PRACTICE_USER, CLIENT_USER, MEDIDATA_USER
from .forms import PracticePreferencesForm
from permissions.functions import access_user_management
from organisations.models import OrganisationGeneralPractice

from django.conf import settings
DEFAULT_FROM = settings.DEFAULT_FROM
ACCOUNT_LINK = settings.ACCOUNT_LINK

from .functions import change_role, remove_user, get_table_data,\
        get_post_new_user_data, get_user_type_form, reset_password


@login_required(login_url='/accounts/login')
def account_view(request):
    header_title = 'Account'
    user = request.user
    gp_user = GeneralPracticeUser.objects.get(pk=user.userprofilebase.generalpracticeuser.pk)
    gp_organisation = gp_user.organisation
    try:
        practice_preferences = PracticePreferences.objects.get(gp_organisation=gp_organisation)
    except PracticePreferences.DoesNotExist:
        practice_preferences = PracticePreferences()
        practice_preferences.gp_organisation = gp_organisation
        practice_preferences.notification = 'NEW'
        practice_preferences.save()
    
    if request.is_ajax():
        gp_preferences_form = PracticePreferencesForm(request.POST, instance=practice_preferences)
        if gp_preferences_form.is_valid():
            gp_preferences_form.save()
            return JsonResponse({'message': 'Preferences have been saved.'})

    gp_preferences_form = PracticePreferencesForm(instance=practice_preferences)
    
    organisation = multi_getattr(user, 'userprofilebase.generalpracticeuser.organisation', default=None)
    organisation_fee = OrganisationFee.objects.filter(gp_practice=organisation).first()
    organisation_fee_data = list()

    if organisation_fee:
        organisation_fee_data.append('0-{max_day_level_1} days @ £{amount_rate_level_1}'.format(
            max_day_level_1=organisation_fee.max_day_lvl_1,
            amount_rate_level_1=organisation_fee.amount_rate_lvl_1)
        )
        organisation_fee_data.append('{min_day_level_2}-{max_day_level_2} days @ £{amount_rate_level_2}'.format(
            min_day_level_2=organisation_fee.max_day_lvl_1+1,
            max_day_level_2=organisation_fee.max_day_lvl_2,
            amount_rate_level_2=organisation_fee.amount_rate_lvl_2)
        )
        organisation_fee_data.append('{min_day_level_3}-{max_day_level_3} days @ £{amount_rate_level_3}'.format(
            min_day_level_3=organisation_fee.max_day_lvl_2 + 1,
            max_day_level_3=organisation_fee.max_day_lvl_3,
            amount_rate_level_3=organisation_fee.amount_rate_lvl_3)
        )
        organisation_fee_data.append('{max_day_level_4} days or more @ £{amount_rate_level_4}'.format(
            max_day_level_4=organisation_fee.max_day_lvl_4,
            amount_rate_level_4=organisation_fee.amount_rate_lvl_4)
        )

    return render(request, 'accounts/accounts_view.html', {
        'header_title': header_title,
        'organisation_fee_data': organisation_fee_data,
        'gp_preferences_form': gp_preferences_form
    })


@login_required(login_url='/accounts/login')
def manage_user(request):
    if request.method == "POST":
        action_type = request.POST.get("action_type")
        if action_type == "Remove":
            remove_user(request)

        elif action_type == "Change":
            change_role(request)

        elif action_type == "Reset Password":
            reset_password(request)

        return JsonResponse({"success": "true"})


@login_required(login_url='/accounts/login')
@access_user_management('organisations.view_user_management')
def view_users(request):
    header_title = "User Management"
    profiles = UserProfileBase.all_objects.all()
    user = request.user
    user = User.objects.get(username=user.username)
    user_profile = UserProfileBase.objects.filter(user_id=user.pk).first()

    if 'status' in request.GET:
        filter_type = request.GET.get('type', 'active')
        filter_status = request.GET.get('status', -1)
        filter_user_type = request.GET.get('user_type', None)
        if filter_status == 'undefined':
            filter_status = -1
        else:
            filter_status = int(filter_status)
        if filter_type == 'undefined':
            filter_type = 'active'
    else:
        filter_type = request.COOKIES.get('type')
        filter_status = int(request.COOKIES.get('status', -1))
        filter_user_type = request.COOKIES.get('user_type', None)


    if filter_type == '':
        filter_type = "active"
    user_types = [MEDIDATA_USER, CLIENT_USER, GENERAL_PRACTICE_USER]
    query_set = user.get_query_set_within_organisation().filter(type__in=user_types)

    if filter_type == 'active':
        query_set = query_set.filter(userprofilebase__in=profiles.alive())
    elif filter_type == 'deactivated':
        query_set = query_set.filter(userprofilebase__in=profiles.dead())

    filter_query = query_set
    if filter_status != -1:
        if (filter_user_type and filter_user_type == GENERAL_PRACTICE_USER) or hasattr(user.userprofilebase, 'generalpracticeuser'):
            filter_query = query_set.filter(userprofilebase__generalpracticeuser__role=filter_status)
        elif (filter_user_type and filter_user_type == CLIENT_USER) or hasattr(user.userprofilebase, 'clientuser'):
            filter_query = query_set.filter(userprofilebase__clientuser__role=filter_status)
        else:
            filter_query = query_set.filter(type=MEDIDATA_USER)

    table_data = get_table_data(user, query_set, filter_query)
    RequestConfig(request, paginate={'per_page': 5}).configure(table_data['table'])
    table_data['table'].order_by = request.GET.get('sort', '-created')
    permission_formset = []
    if user_profile and hasattr(user_profile, 'generalpracticeuser'):
        organisation = user_profile.generalpracticeuser.organisation
        permissions = InstructionPermission.objects.filter(organisation=organisation)
        permission_set = modelformset_factory(InstructionPermission, form=InstructionPermissionForm, extra=(3-permissions.count()))
        initial_data = set_initial_data_permission(permissions, organisation.pk)
        permission_formset = permission_set(queryset=permissions, initial=initial_data)
    elif user_profile and hasattr(user_profile, 'medidatauser'):
        permissions = InstructionPermission.objects.filter(global_permission=True)
        permission_set = modelformset_factory(InstructionPermission, form=InstructionPermissionForm, extra=(3-permissions.count()))
        initial_data = set_initial_data_permission(permissions, None)
        permission_formset = permission_set(queryset=permissions, initial=initial_data)

    show_pop_up = ''
    if request.GET.get('show'):
        show_pop_up = 'show'

    response = render(request, 'user_management/user_management.html', {
        'user': user,
        'header_title': header_title,
        'table': table_data['table'],
        'overall_users_number': table_data['overall_users_number'],
        'permission_formset': permission_formset,
        'user_type': table_data['user_type'],
        'show_pop_up': show_pop_up
    })
    return response


def set_initial_data_permission(permissions, organisation_id):
    initial_data = []
    for key, value in GeneralPracticeUser.ROLE_CHOICES:
        if key is '': continue
        if key not in permissions.values('role'):
            initial_data.append({'organisation': organisation_id, 'role': key})
    return initial_data


@login_required(login_url='/accounts/login')
@access_user_management('permissions.change_instructionpermission')
def update_permission(request):
    request.META['HTTP_REFERER'] = ''
    if request.method == 'POST':
        user = request.user
        user = User.objects.get(pk=user.id)
        user_profile = UserProfileBase.objects.filter(user_id=user.pk).first()
        permission_set = modelformset_factory(InstructionPermission, form=InstructionPermissionForm, extra=0)
        permission_formset = permission_set(request.POST, form_kwargs={'empty_permitted': False})
        if permission_formset.is_valid():
            for form in permission_formset:
                if user.type == MEDIDATA_USER:
                    set_all_permissions(request, form)
                else:
                    set_permission(request, form)
    response = redirect('accounts:view_users')
    response['Location'] += "?show=True"
    return response


def set_all_permissions(request, form):
    permission = form.save(commit=False)
    data = form.cleaned_data
    for organisation in OrganisationGeneralPractice.objects.filter(accept_policy= True, live=True):
        gp_permission, create = InstructionPermission.objects.get_or_create(organisation=organisation, role=permission.role)
        data['name'] = '%s : %s'%(permission.get_role_display(),organisation.__str__())
        if gp_permission.group:
            group_form = GroupPermissionForm(data, instance=gp_permission.group)
        else:
            group_form = GroupPermissionForm(data)

        if group_form.is_valid():
            group = group_form.save()
            gp_permission.group = group
            gp_permission.save()
            gp_permission.allocate_permission_to_gp()

    data['name'] = '%s : MediData'%permission.get_role_display()
    if permission.group:
        group_form = GroupPermissionForm(data, instance=gp_permission.group)
    else:
        group_form = GroupPermissionForm(data)

    if group_form.is_valid():
        group = group_form.save()
        permission.group = group
        permission.global_permission = True
        permission.save()


def set_permission(request, form):
    permission = form.save(commit=False)
    data = form.cleaned_data
    data['name'] = permission.__str__()
    if permission.group:
        group_form = GroupPermissionForm(data, instance=permission.group)
    else:
        group_form = GroupPermissionForm(data)
    group = group_form.save()
    permission.group = group
    permission.save()
    permission.allocate_permission_to_gp()


@login_required(login_url='/accounts/login')
@access_user_management('organisations.add_user_management')
def create_user(request):
    header_title = "Add New User"

    cur_user = request.user
    cur_user = User.objects.get(username=cur_user.username)

    if request.method == 'POST':
        user_role = request.POST.get("user_role")
        new_user_data = get_post_new_user_data(cur_user, request, user_role)
        organisation = new_user_data['organisation']
        newuser_form = new_user_data['newuser_form']
        user_type = new_user_data['user_type']

        if not user_role:
            messages.warning(request, 'Please input all the fields properly.')
        elif newuser_form.is_valid():
            user = User.objects.filter(
                Q(username=newuser_form.cleaned_data['username']) |
                Q(email=newuser_form.cleaned_data['email'])
            )
            if not user.exists():
                user = User.objects.create(
                    first_name=newuser_form.cleaned_data['first_name'],
                    last_name=newuser_form.cleaned_data['last_name'],
                    username=newuser_form.cleaned_data['username'],
                    email=newuser_form.cleaned_data['email']
                )
                user.type = user_type
                user.is_staff = new_user_data['is_staff']

                user.set_password(newuser_form.cleaned_data['password'])
                user.save()
                newuser = newuser_form.save(commit=False)
                newuser.organisation = organisation
                newuser.role = user_role
                newuser.user = user
                newuser.save()
                reset_password_form = PasswordResetForm(data={'email': user.email})
                if newuser_form.cleaned_data['send_email'] and reset_password_form.is_valid():
                    reset_password_form.save(
                        request=request,
                        from_email=DEFAULT_FROM,
                        subject_template_name='registration/password_reset_subject_new.txt',
                        email_template_name='registration/password_reset_email_new.html')
                messages.success(request, 'New User Account created successfully.')
                return redirect("accounts:view_users")
            else:
                messages.warning(request, 'User Account Existing In Database')
        else:
            messages.warning(request, 'Please input all the fields properly.')

    user_type_form = get_user_type_form(cur_user)
    newuser_form = user_type_form['newuser_form']
    user_type = user_type_form['user_type']

    response = render(request, 'user_management/new_user.html', {
        'header_title': header_title,
        'newuser_form': newuser_form,
        'user_type': user_type
    })

    return response


@login_required(login_url='/accounts/login')
@access_user_management('organisations.change_user_management')
def medi_change_user(request, email):
    user = User.objects.filter(email=email).first()
    initial_data = {
        'user_type': user.type,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
        'password': user.password
    }
    if hasattr(user, 'userprofilebase'):
        user_profile = user.userprofilebase
        if hasattr(user_profile, 'generalpracticeuser'):
            gp = user.userprofilebase.generalpracticeuser
            initial_data['gp_organisation'] = gp.organisation
            initial_data['payment_bank_holder_name'] = gp.payment_bank_holder_name
            initial_data['payment_bank_sort_code'] = gp.payment_bank_sort_code
            initial_data['payment_bank_account_number'] = gp.payment_bank_account_number
            initial_data['role'] = gp.role
        elif hasattr(user_profile, 'clientuser'):
            client = user.userprofilebase.clientuser
            initial_data['client_organisation'] = client.organisation
            initial_data['role'] = client.role
        elif hasattr(user_profile, 'medidatauser'):
            organisation = user.userprofilebase.medidatauser.organisation
            initial_data['medi_organisation'] = organisation

    if request.method == 'POST':
        newuser_form = AllUserForm(request.POST)
        if newuser_form.is_valid():
            data = newuser_form.cleaned_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.save()
            if data['user_type'] == GENERAL_PRACTICE_USER:
                gp = user.userprofilebase.generalpracticeuser
                user_form = NewGPForm(request.POST, instance=gp)
                organisation = data['gp_organisation']
            elif data['user_type'] == CLIENT_USER:
                client = user.userprofilebase.clientuser
                user_form = NewClientForm(request.POST, instance=client)
                organisation = data['client_organisation']
            else:
                medi = user.userprofilebase.medidatauser
                user_form = NewMediForm(request.POST, instance=medi)
                organisation = data['medi_organisation']
            if user_form.is_valid():
                newuser = user_form.save(commit=False)
                newuser.organisation = organisation
                if user.type != MEDIDATA_USER:
                    newuser.role = data.get('role')
                newuser.save()
                messages.success(request, 'User updated successfully.')
                return redirect("accounts:view_users")
            else:
                messages.warning(request, user_form.errors)

    newuser_form = AllUserForm(initial=initial_data)
    response = render(request, 'user_management/medi_update_user.html',{
        'newuser_form': newuser_form,
        'user': user,
    })
    return response


@login_required(login_url='/accounts/login')
@access_user_management('organisations.add_user_management')
def medi_create_user(request):
    newuser_form = AllUserForm()
    if request.method == 'POST':
        newuser_form = AllUserForm(request.POST)
        if newuser_form.is_valid():
            data = newuser_form.cleaned_data
            user = User.objects.filter(
                Q(username=data['username']) |
                Q(email=data['email'])
            )
            if not user.exists():
                user = User.objects.create(
                    first_name=newuser_form.cleaned_data['first_name'],
                    last_name=newuser_form.cleaned_data['last_name'],
                    username=newuser_form.cleaned_data['username'],
                    email=newuser_form.cleaned_data['email'],
                    type=data['user_type']
                )
                user.set_password(newuser_form.cleaned_data['password'])
                user.save()
                if data['user_type'] == GENERAL_PRACTICE_USER:
                    user_form = NewGPForm(request.POST)
                    organisation = data['gp_organisation']
                elif data['user_type'] == CLIENT_USER:
                    user_form = NewClientForm(request.POST)
                    organisation = data['client_organisation']
                else:
                    user_form = NewMediForm(request.POST)
                    organisation = data['medi_organisation']
                if user_form.is_valid():
                    newuser = user_form.save(commit=False)
                    newuser.organisation = organisation
                    if user.type != MEDIDATA_USER:
                        newuser.role = data.get('role')
                    newuser.user = user
                    newuser.save()
                    reset_password_form = PasswordResetForm(data={'email': user.email})
                    if newuser_form.cleaned_data['send_email'] and reset_password_form.is_valid():
                        reset_password_form.save(
                            request=request,
                            from_email=DEFAULT_FROM,
                            subject_template_name='registration/password_reset_subject_new.txt',
                            email_template_name='registration/password_reset_email_new.html')
                    messages.success(request, 'New User Account created successfully.')
                    return redirect("accounts:view_users")
                else:
                    messages.warning(request, user_form.errors)
            else:
                messages.warning(request, 'User Account Existing In Database')
    response = render(request, 'user_management/medi_create_user.html',{
        'newuser_form': newuser_form,
    })
    return response


def verify_password(request):
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    surname = request.POST.get('surname')
    email = request.POST.get('email')
    results = verify_pass(password, first_name, surname, email)
    return JsonResponse({'results': results})


def check_email(request):
    email = request.POST.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
