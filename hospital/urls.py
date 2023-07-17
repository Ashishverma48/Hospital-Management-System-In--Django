from django.urls import path
from .views import *
urlpatterns = [

# HOME PAGE
    path('',viewHome,name='home'),
    path('login/',ViewLogin,name='login'),
    path('logout/',ViewLogout,name='logout'),

# ADMIN LOGIN
    path('admin-login/',ViewAdminLogin,name='adminlogin'),
    path('admin-signup/',ViewAdminSignup,name='adminsignup'),

# ADMIN DASHBOARD PANEL
    path('admin-dash/',ViewAdminDashboard,name='admindashboard'),
    path('admin-dash-main/',ViewAdminDashboardMain,name='admindashboardMain'),
     
#ADMIN  DASHBOARD DOCTORS
    path('admin-dash-patient/',ViewAdminDashboardPatient,name='admindashboardPatient'),
    path('admin-dash-doctor/',ViewAdminDashboardDoctor,name='admindashboardDoctor'),
    path('admin-doctor/',ViewAdmindDoctor,name='adminDoctor'),
    path('admin-doctor-add/',ViewAdmindDoctorAdd,name='adminDoctorAdd'),
    path('admin-doctor-delete/<int:id>/',ViewAdminDoctorDelete,name='admindoctordelete'),
    path('admin-doctor-update/<int:id>/',ViewAdminDoctorUpdate,name='admindoctorupdate'),
    path('admin-doctor-approve/',ViewAdmindDoctorApprove,name='adminDoctorApprove'),
    path('admin-doctor-approve/<int:id>/',ViewDoctorApprove,name='DoctorApprove'),
    path('admin-doctor-reject/<int:id>/',ViewDoctorReject,name='DoctorReject'),

 #ADMIN  DASHBOARD PATIENT
    path('admin-patient/',ViewAdmindPatient,name='adminPatient'),
    path('admin-patient-add/',ViewAdmindPatientAdd,name='adminPatientAdd'),
    path('admin-patient-approvel/',ViewAdminPatientApprovevel,name='adminPatientApprovel'),
    path('admin-patient-approve/<int:id>',ViewAdminPatientApprove,name='PatientApprove'),
    path('admin-patient-reject/<int:id>',ViewAdminPatientReject,name='PatientReject'),
    path('admin-patient-update/<int:id>',ViewAdminPatientUpdate,name='PatientUpdate'),
    path('admin-patient-delete/<int:id>',ViewAdminPatientDelete,name='PatientDelete'),

 #ADMIN  DASHBOARD APPOINTMENT
    path('admin-dash-appointment/',ViewAdminDashboardAppointment,name='admindashboardApppintment'),
    path('admin-add-appointment/',ViewAdminAddAppointment,name='adminAddAppointment'),
    path('admin-view-appointment/',ViewAdminViewAppointment,name='adminViewAppointment'),
    path('admin-approvel-appointment/',ViewAdminApprovelAppointment,name='adminApprovelAppointment'),
    path('admin-approve-appointment/<int:id>',ViewAdminApproveAppointment,name='AppointmentApprove'),
    path('admin-reject-appointment/<int:id>',ViewAdminRejectAppointment,name='AppointmentReject'),
 
 #ADMIN  DASHBOARD GALLERY
   path('admin-gallery/',ViewAdminGalleryDashBoard,name='adminGalleryDashboard'),
   path('add-image/',ViewAdminAddNewImages,name='adminAddNewImage'),

 #ADMIN  DASHBOARD INQUERY
   path('admin-inquery/',ViewInqueryDashboard,name='adminInquery'),

 #ADMIN  DASHBOARD DISCHARGE
    path('admin-discharge-patient/',ViewAdminPatientDischarge,name='PatientDischarge'),



# SHOW ALL IMAGES PAGE 
    path('images',ShowAllImages,name='images'),



# DOCTOR SIGNUP & LOGIN
    path('doctor-signup/',ViewDoctorSignup,name='doctorsignup'),
    path('doctor-login/',ViewDoctorLogin,name='doctorlogin'),

 #DOCTOR  DASHBOARD DOCTORS
    path('doctor-dash/',ViewDoctorDashBoard,name='doctorDash'),
    path('doctor-dash-patient/',ViewDoctorDashBoardPatient,name='doctorDashPatient'),
    path('doctor-dash-patient-view/',ViewDoctorDashBoardPatientRecord,name='doctorDashPatientRecord'),
    path('doctor-dash-appointment/',ViewDoctorDashBoardAppointMent,name='doctorDashAppointMent'),
    path('doctor-dash-appointment-delete/<int:id>',ViewDoctorDashBoardAppointMentRemove,name='doctorDashAppointMentRemove'),

# PATIENT LOGIN & SIGNUP
    path('patient-signup/',ViewPatientSignup,name='patientsignup'),
    path('patient-login/',ViewPatientLogin,name='patientlogin'),

# PATIENT DASHBOARD 
    path('patient-dash/',ViewPatientDashBoard,name='patientDashBoard'),
    path('patient-dash-appointment/',ViewPatientDashAppointment,name='patientDashBoardAppointment'),
    path('patient-book-appointment/',ViewPatientBookAppointment,name='patientBookAppointment'),
]
