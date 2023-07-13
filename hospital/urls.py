from django.urls import path
from .views import *
urlpatterns = [
    
    path('',viewHome,name='home'),
    path('login/',ViewLogin,name='login'),
    path('admin-login/',ViewAdminLogin,name='adminlogin'),
    path('admin-signup/',ViewAdminSignup,name='adminsignup'),
    path('admin-dash/',ViewAdminDashboard,name='admindashboard'),
    path('admin-dash-main/',ViewAdminDashboardMain,name='admindashboardMain'),
    path('admin-dash-appointment/',ViewAdminDashboardAppointment,name='admindashboardApppintment'),
    path('admin-dash-patient/',ViewAdminDashboardPatient,name='admindashboardPatient'),
    path('admin-dash-doctor/',ViewAdminDashboardDoctor,name='admindashboardDoctor'),
    path('admin-doctor/',ViewAdmindDoctor,name='adminDoctor'),
    path('admin-patient/',ViewAdmindPatient,name='adminPatient'),
    path('admin-doctor-delete/<int:id>/',ViewAdminDoctorDelete,name='admindoctordelete'),
    path('admin-doctor-update/<int:id>/',ViewAdminDoctorUpdate,name='admindoctorupdate'),
    
    path('doctor-signup/',ViewDoctorSignup,name='doctorsignup'),
    path('doctor-login/',ViewDoctorLogin,name='doctorlogin'),

    path('patient-signup/',ViewPatientSignup,name='patientsignup'),
    path('patient-login/',ViewPatientLogin,name='patientlogin'),


]
