from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect
from django.http import JsonResponse

from common.functions import multi_getattr, get_env_variable
from payment.models import OrganisationFee
from django_tables2 import RequestConfig

from .models import User, UserProfileBase, GeneralPracticeUser
from .models import GENERAL_PRACTICE_USER, CLIENT_USER
from .forms import NewGPForm, NewClientForm
from .tables import GPUserTable, ClientUserTable

from django.conf import settings
DEFAULT_FROM = settings.DEFAULT_FROM
ACCOUNT_LINK = settings.ACCOUNT_LINK

from .functions import reset_password, change_role, remove_user
from .functions import count_gpusers, count_clientusers, get_table_data
from .functions import get_post_new_user_data, get_user_type_form
from .functions import get_users_count


@login_required(login_url='/accounts/login')
def account_view(request):
    header_title = 'Account'
    user = request.user
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
        organisation_fee_data.append('{max_day_level_3} days or more @ £{amount_rate_level_3}'.format(
            max_day_level_3=organisation_fee.max_day_lvl_3,
            amount_rate_level_3=organisation_fee.amount_rate_lvl_3)
        )

    return render(request, 'accounts/accounts_view.html', {
        'header_title': header_title,
        'organisation_fee_data': organisation_fee_data,
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
def view_users(request):
    header_title = "User Management"
    profiles = UserProfileBase.all_objects.all()
    user = request.user
    user = User.objects.get(username=user.username)

    if 'status' in request.GET:
        filter_type = request.GET.get('type', 'active')
        filter_status = request.GET.get('status', -1)
        if filter_status == 'undefined':
            filter_status = -1
        else:
            filter_status = int(filter_status)        
        if filter_type == 'undefined':
            filter_type = 'active'
    else:
        filter_type = request.COOKIES.get('type')
        filter_status = int(request.COOKIES.get('status', -1))

    if filter_type == '':
        filter_type = "active"
    query_set = user.get_query_set_within_organisation()

    if filter_type == 'active':
        query_set = query_set.filter(userprofilebase__in=profiles.alive())
    elif filter_type == 'deactivated':
        query_set = query_set.filter(userprofilebase__in=profiles.dead())

    overall_users_number = get_users_count(user, query_set)
    
    if filter_status != -1:
        if hasattr(user.userprofilebase, 'generalpracticeuser'):
            query_set = query_set.filter(userprofilebase__generalpracticeuser__role=filter_status)
        elif hasattr(user.userprofilebase, 'clientuser'):
            query_set = query_set.filter(userprofilebase__clientuser__role=filter_status)
        
    table_data = get_table_data(user, query_set)
    RequestConfig(request, paginate={'per_page': 5}).configure(table_data['table'])
    table_data['table'].order_by = request.GET.get('sort', '-created')

    response = render(request, 'user_management/user_management.html', {
        'user': user,
        'header_title': header_title,
        'table': table_data['table'],
        'overall_users_number': overall_users_number,
        'user_type': table_data['user_type']
    })

    return response


@login_required(login_url='/accounts/login')
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
                to_email = newuser_form.cleaned_data['email']
                newuser = newuser_form.save(commit=False)
                newuser.organisation = organisation
                newuser.role = user_role
                newuser.user = user
                newuser.save()
                if newuser_form.cleaned_data['send_email']:
                    send_mail(
                        'New Account',
                        'You have a new Account. Click here {} to see it.'.format(ACCOUNT_LINK),
                        DEFAULT_FROM,
                        [to_email],
                        fail_silently=False,
                        auth_user=get_env_variable('SENDGRID_USER'),
                        auth_password=get_env_variable('SENDGRID_PASS'),
                    )
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