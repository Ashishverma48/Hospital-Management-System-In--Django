from django.urls import path
from .views import *
urlpatterns = [
    
    path('',viewHome,name='home'),
    # ADMIN PANAL
    path('login/',ViewLogin,name='login'),
    path('logout/',ViewLogout,name='logout'),
    path('admin-login/',ViewAdminLogin,name='adminlogin'),
    path('admin-signup/',ViewAdminSignup,name='adminsignup'),
    path('admin-dash/',ViewAdminDashboard,name='admindashboard'),
    path('admin-dash-main/',ViewAdminDashboardMain,name='admindashboardMain'),
    
    path('admin-dash-patient/',ViewAdminDashboardPatient,name='admindashboardPatient'),
    path('admin-dash-doctor/',ViewAdminDashboardDoctor,name='admindashboardDoctor'),
    path('admin-doctor/',ViewAdmindDoctor,name='adminDoctor'),
    path('admin-doctor-add/',ViewAdmindDoctorAdd,name='adminDoctorAdd'),
    path('admin-doctor-delete/<int:id>/',ViewAdminDoctorDelete,name='admindoctordelete'),
    path('admin-doctor-update/<int:id>/',ViewAdminDoctorUpdate,name='admindoctorupdate'),
    path('admin-doctor-approve/',ViewAdmindDoctorApprove,name='adminDoctorApprove'),
    path('admin-doctor-approve/<int:id>/',ViewDoctorApprove,name='DoctorApprove'),
    path('admin-doctor-reject/<int:id>/',ViewDoctorReject,name='DoctorReject'),

    path('admin-patient/',ViewAdmindPatient,name='adminPatient'),
    path('admin-patient-add/',ViewAdmindPatientAdd,name='adminPatientAdd'),
    path('admin-patient-approvel/',ViewAdminPatientApprovevel,name='adminPatientApprovel'),
    path('admin-patient-approve/<int:id>',ViewAdminPatientApprove,name='PatientApprove'),
    path('admin-patient-reject/<int:id>',ViewAdminPatientReject,name='PatientReject'),
    path('admin-patient-update/<int:id>',ViewAdminPatientUpdate,name='PatientUpdate'),
    path('admin-patient-delete/<int:id>',ViewAdminPatientDelete,name='PatientDelete'),

    path('admin-dash-appointment/',ViewAdminDashboardAppointment,name='admindashboardApppintment'),
    path('admin-add-appointment/',ViewAdminAddAppointment,name='adminAddAppointment'),
    path('admin-view-appointment/',ViewAdminViewAppointment,name='adminViewAppointment'),
    path('admin-approvel-appointment/',ViewAdminApprovelAppointment,name='adminApprovelAppointment'),
    path('admin-approve-appointment/<int:id>',ViewAdminApproveAppointment,name='AppointmentApprove'),
    path('admin-reject-appointment/<int:id>',ViewAdminRejectAppointment,name='AppointmentReject'),







    path('doctor-signup/',ViewDoctorSignup,name='doctorsignup'),
    path('doctor-login/',ViewDoctorLogin,name='doctorlogin'),



    path('patient-signup/',ViewPatientSignup,name='patientsignup'),
    path('patient-login/',ViewPatientLogin,name='patientlogin'),


]
