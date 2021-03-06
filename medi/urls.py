"""medi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from instructions.views import instruction_pipeline_view
from accounts.functions import notify_admins
from django.contrib.auth import views as auth_views

admin.site.site_header = 'MediData administration'
admin.site.site_title = 'MediData administration'


urlpatterns = [
    path('', instruction_pipeline_view, name='view_pipeline'),
    path('testservices/', include('services.urls')),
    path('medicalreport/', include('medicalreport.urls')),
    path('snomedct/', include('snomedct.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('instruction/', include('instructions.urls', namespace='instructions')),
    path('onboarding/', include('onboarding.urls', namespace='onboarding')),
    path('organisation/', include('organisations.urls', namespace='organisations')),
    path('template/', include('template.urls', namespace='template')),
    path('report/', include('report.urls', namespace='report')),
    path('select2/', include('django_select2.urls')),
    path('password_change/done/', notify_admins(auth_views.PasswordChangeDoneView.as_view()), name='password_change_done'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
