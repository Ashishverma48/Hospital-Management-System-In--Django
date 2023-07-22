from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from rest_framework import viewsets
from .serialzers import GallarySerialzers
# Create your views here.

def viewHome(request):
    doctors = Doctor.objects.all().filter(status=True)
    frm_unbound = ContactForm()
    if request.method == 'POST':
        frm_bound = ContactForm(request.POST)
        frm_bound.is_valid()
        frm_bound.save()
        return redirect('home')
    return render(request,'hospital/index.html',locals())

def ViewLogin(request):
    return render(request,'hospital/login.html')

def ViewLogout(request):
    logout(request)

    return redirect('home')

def ViewAdminSignup(request):
    form = AdminForms()
    if request.method == 'POST':
        form  = AdminForms(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return redirect('adminlogin')
    return render(request,'hospital/adminSignup.html',{'form':form})


def ViewDoctorSignup(request):
    userform = DoctorUserForms()
    doctorform = DoctorForm()
    if request.method =='POST':
        userform = DoctorUserForms(request.POST)
        doctorform = DoctorForm(request.POST,request.FILES)
        if userform.is_valid() and doctorform.is_valid():
            password = userform.cleaned_data['password']
            user  = userform.save(commit=False)
            print(password)
            user.set_password(password)
            print(user.password)
            # print(userform.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            return redirect('doctorlogin')
        else:
            return render(request,'hospital/doctorSignup.html',locals())


    return render(request,'hospital/doctorSignup.html',locals())

def ViewPatientSignup(request):
    userform = PatientUserForms()
    patientform = PatientForm()
    if request.method == 'POST':
        userform = PatientUserForms(request.POST)
        patientform = PatientForm( request.POST,request.FILES)
        if userform.is_valid() and patientform.is_valid():
            password  = userform.cleaned_data['password']
            user = userform.save(commit=False)

            user.set_password(password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user  = user
            patient.save()
            my_doctor_group= Group.objects.get_or_create(name='PATIENT')
            my_doctor_group[0].user_set.add(user)
            return redirect('patientlogin')
        else:
            return render(request,'hospital/patientSignup.html',locals())

        

    return render(request,'hospital/patientSignup.html',locals())

# FOR CHEKING USER IS ADMIN, DOCTOR AND PATIENT
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()




def ViewAdminLogin(request):
    if request.method == 'POST':

        username = request.POST.get('adminUserName')
        password = request.POST.get('adminPassword')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if is_admin(user):
                return redirect('admindashboard')
            
            

        
    return render(request,'hospital/adminLogin.html')

def ViewDoctorLogin(request):
    if request.method == 'POST':

        username = request.POST.get('adminUserName')
        password = request.POST.get('adminPassword')
        selectuser = request.POST.get('user')

        
        print(username,password,selectuser)
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            print(user.groups.name)
            login(request,user)
           
            if is_doctor(user):
                approvel = Doctor.objects.filter(user_id=request.user.id,status = True)
                if approvel:
                    return redirect('doctorDash')
                else:
                    messages.warning(request,'Wait For Approvel')
        else:
            messages.warning(request,'UserId & Password Not Match !')
            
        return render(request,'hospital/doctorLogin.html')
    return render(request,'hospital/doctorLogin.html')

def ViewPatientLogin(request):
    if request.method == 'POST':

        username = request.POST.get('adminUserName')
        password = request.POST.get('adminPassword')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
          
            if is_patient(user):
                approvel = Patient.objects.all().filter(user_id=request.user.id,status=True)
                if approvel:
                    return redirect('patientDashBoard')
                else:
                    messages.warning(request,'Wait For Approvel')
        else:
            messages.warning(request,'UserId & Password Not Match !')

            
    return render(request,'hospital/patientLogin.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDashboard(request):
    # Doctor 
    doctors = Doctor.objects.all()
    doctorNum = Doctor.objects.all().count()
    # Patient 
    patients= Patient.objects.all()
    patientNum = Patient.objects.all().count()
    return render(request,'hospital/adminDashboard.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDashboardMain(request):
    doctors = Doctor.objects.all()
    doctorApprovedNum = Doctor.objects.all().filter(status = True).count()
    doctorPendingNum = Doctor.objects.all().filter(status = False).count()
    # Patient 
    

    patients= Patient.objects.all()
    patientApprovedNum = Patient.objects.all().filter(status=True).count()
    patientPendingNum = Patient.objects.all().filter(status=False).count()

    appointmentApproveNum = Appointment.objects.all().filter(status=True).count()
    appointmentPendingNum = Appointment.objects.all().filter(status=False).count()
    return render(request,'hospital/adminDashboardMain.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdmindDoctor(request):
    doctors = Doctor.objects.all().filter(status=True)
    return render(request,'hospital/adminDoctor.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDoctorUpdate(request,id):
    
    doctor = Doctor.objects.get(user_id=id)
    user = User.objects.get(id=doctor.user_id)       
    userform = DoctorUserForms(instance=user)
    doctorform = DoctorForm(request.FILES,instance = doctor)
    if request.method=='POST':
        userform = DoctorUserForms(request.POST,instance=user)
        doctorform = DoctorForm(request.POST,request.FILES,instance = doctor)
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctorfrm = doctorform.save(commit=False)
            doctorfrm.status=True
            doctorfrm.save()
            return redirect('admindashboardDoctor')
        return render(request,'hospital/adminDoctorUpdate.html',locals())



    # doctors = Doctor.objects.all()
    return render(request,'hospital/adminDoctorUpdate.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDoctorDelete(request,id):
    doctor = Doctor.objects.get(user_id=id)
    user = User.objects.get(id=id)
    user.delete()
    doctor.delete()
    
    return redirect('admindashboardDoctor ')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDashboardAppointment(request):
    
    return render(request,'hospital/adminAppointment.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDashboardPatient(request):

    return render(request,'hospital/adminDashboardPatient.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminDashboardDoctor(request):

    return render(request,'hospital/adminDashboardDoctor.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdmindPatient(request):
    patients = Patient.objects.all().filter(status=True)
    print(patients)
    return render(request,'hospital/adminPatient.html',locals())
    
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdmindDoctorAdd(request):
    userform = DoctorUserForms()
    doctorform = DoctorForm()
    if request.method == 'POST':
        userform = DoctorUserForms(request.POST)
        doctorform = DoctorForm(request.POST,request.FILES)
        if userform.is_valid and doctorform.is_valid():
            user  = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.save()
            doctor_group = Group.objects.get_or_create(name='DOCTOR')
            doctor_group[0].user_set.add(user)
            return redirect('adminDoctor')

    return render(request,'hospital/adminRegisterDoctor.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdmindDoctorApprove(request):
    doctors = Doctor.objects.all().filter(status=False)
    return render(request,'hospital/adminApproveDoctor.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewDoctorApprove(request,id):
    doctors = Doctor.objects.get(id=id)
    doctors.status=True
    doctors.save()
    print(doctors)
    return redirect('adminDoctor')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewDoctorReject(request,id):
    doctor = Doctor.objects.get(id=id)
    user = User.objects.get(id=doctor.user_id)
    doctor.delete()
    user.delete()
    return redirect('adminDoctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdmindPatientAdd(request):
    userform = PatientUserForms()
    patientform = PatientForm()
    if request.method=='POST':
        userform = PatientUserForms(request.POST)
        patientform = PatientForm(request.POST,request.FILES)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)
            return redirect('adminPatient')
    return render(request,'hospital/adminRegisterPatient.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminPatientApprovevel(request):
    patients = Patient.objects.all().filter(status=False)
    return render(request,'hospital/patientApprovel.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminPatientApprove(request,id):
    patient = Patient.objects.get(id=id)
    patient.status = True
    patient.save()
    return redirect('adminPatient')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminPatientReject(request,id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    patient.delete()
    user.delete()
    return redirect('adminPatient')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminPatientUpdate(request,id):
    patientid = Patient.objects.get(id=id)
    userid = User.objects.get(id=patientid.user_id)
    userform = PatientUserForms(instance = userid)
    patientform = PatientForm(instance = patientid)
    if request.method == 'POST':
        userform = PatientUserForms(request.POST,instance = userid)
        patientform = PatientForm(request.POST,request.FILES,instance=patientid)
        if userform.is_valid() and patientform.is_valid():
            user  =  userform.save()
            user.set_password(user.password)
            user.save()
            patient  = patientform.save(commit=False)
            patient.user  = user
            patient.save()
            messages.success(request,'Patient Update Successfully')
            return redirect('adminPatient')
    return render(request,'hospital/adminPatientUpdate.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminPatientDelete(request,id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    patient.delete()
    user.delete()
    messages.warning(request,'Patient Remove Succesfully')
    return redirect('adminPatient')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminAddAppointment(request):
    frm_unbound = AppointmentForm()
    
    if request.method == 'POST':
        frm_bound = AppointmentForm(request.POST)
        
        if frm_bound.is_valid():
            print('success')
            appointment  = frm_bound.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status  = True
            appointment.save()
            messages.success(request,'Appointment Add Successfully ')
            return redirect('admindashboardApppintment')
        else:
            print('errors')
        
    return render(request,'hospital/adminAddAppointment.html',{'appointment':frm_unbound})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminViewAppointment(request):
    appointment = Appointment.objects.all().filter(status=True)
    return render(request,'hospital/adminViewAppointment.html',locals())


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminApprovelAppointment(request):
    appointment = Appointment.objects.all().filter(status=False)
    return render(request,'hospital/adminApprovelAppointment.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminApproveAppointment(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = True
    appointment.save()
    print('approve')
    return redirect('adminViewAppointment')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminRejectAppointment(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    print('delete')
    return redirect('adminViewAppointment')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminPatientDischarge(request):
    patients = Patient.objects.all().filter(status=True)
    return render(request,'hospital/adminDischargePatient.html',locals())


class GallaryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallarySerialzers

def ShowAllImages(request):
    images = Gallery.objects.all()
    return render(request,'hospital/showAllImages.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminGalleryDashBoard(request):
    images = Gallery.objects.all()
    return render(request,'hospital/adminGallery.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewAdminAddNewImages(request):
    images = GalleryForm()
    if request.method =="POST":
        image = GalleryForm(request.POST,request.FILES)
        if image.is_valid():
            image.save()
            messages.success(request,'Image Add Successfull')
            return redirect('adminGalleryDashboard')
    return render(request,'hospital/adminAddImage.html',locals())

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def ViewInqueryDashboard(request):
    inquery  = Contact.objects.all().order_by("-id")
    return render(request,'hospital/adminInquery.html',locals())\
    




# Doctor DashBoard Start

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def ViewDoctorDashBoard(request):
    patientCount = Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentCount = Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    appointment=Appointment.objects.all().filter(status = True,doctorId=request.user.id)
    patientid = []
    for i in appointment:
        patientid.append(i.patientId)
    patient  = Patient.objects.filter(status=True,user_id__in=patientid).order_by('-id')
    appointments = zip(appointment,patient)
    return render(request,'hospital/doctorDashBoard.html',locals())


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def ViewDoctorDashBoardPatient(request):
    return render(request,'hospital/doctorDashBoardPatient.html')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def ViewDoctorDashBoardPatientRecord(request):
    patients = Patient.objects.all().filter(status =True,assignedDoctorId=request.user.id)
    data = {'patients':patients}
    if request.method=="POST":
        search  = request.POST.get('seachPatient')
        patients = Patient.objects.search_by_first_name(search)
        print(patients)
        data = {'patients':patients}

    return render(request,'hospital/doctorDashPatientRecord.html',data)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def ViewDoctorDashBoardAppointMent(request):
    appointment  =Appointment.objects.all().filter(status = True,doctorId = request.user.id)
    patientid = []
    for i in appointment:
        patientid.append(i.patientId)
    patient = Patient.objects.filter(status=True,user_id__in=patientid)
    appointments = zip(appointment,patient)
    return render(request,'hospital/doctorDashAppoitmentRecord.html',{'appointments':appointments})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def ViewDoctorDashBoardAppointMentRemove(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
   
    
   
    
    return redirect('doctorDashAppointMent')
    

# PATIENT DASHBOARD
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def ViewPatientDashBoard(request):
   try:
     patient = Patient.objects.get(user_id = request.user.id)
     doctor = Doctor.objects.get(user_id=patient.assignedDoctorId)
     print(patient,doctor)
     return render(request,'hospital/patientDashboard.html',locals())
   except Exception as Identifier:
    pass
    return render(request,'hospital/patientDashboard.html',locals())

@login_required(login_url='patientlogin')
@user_passes_test(is_patient) 
def ViewPatientDashAppointment(request):
    appointment = Appointment.objects.all().filter(patientId = request.user.id).order_by('-id')
    return render(request,'hospital/patientDashBoardAppointment.html',locals())

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def ViewPatientBookAppointment(request):
    frm_unbound = PatientAppointmentForm()
    data = {
        'form':frm_unbound
    }
    if request.method == 'POST':
        frm_bound = PatientAppointmentForm(request.POST)
        if frm_bound.is_valid():
            app = frm_bound.save(commit=False)
            app.doctorId = request.POST.get('doctorId')
            app.patientId = request.user.id
            app.patientName  = User.objects.get(id=request.user.id).first_name
            app.doctorName = User.objects.get(id=request.POST.get('doctorId')).first_name
            app.save()
            messages.success(request,'Appointment Book Successfully')
            return redirect('patientDashBoardAppointment')

    return render(request,'hospital/patientBookAppointment.html',data)
    



