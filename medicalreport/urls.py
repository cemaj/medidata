from django.urls import path

from . import views

app_name = 'medicalreport'
urlpatterns = [
    path('<int:instruction_id>/patient-emis-number/', views.set_patient_emis_number, name='set_patient_emis_number'),
    path('<int:instruction_id>/select-patient/<int:patient_emis_number>/', views.select_patient, name='select_patient'),
    path('<int:instruction_id>/reject-request/', views.reject_request, name='reject_request'),
    path('<int:instruction_id>/edit/', views.edit_report, name='edit_report'),
    path('<int:instruction_id>/final-report/', views.final_report, name='final_report'),
    path('<int:instruction_id>/view-report/', views.view_report, name='view_report'),
    path('<int:instruction_id>/update/', views.update_report, name='update_report'),
    path('<int:instruction_id>/attachment/<str:path_file>', views.view_attachment, name='view_attachment'),
]
