from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
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
            user = form.save()
            user.set_password(user.password)
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
            user  = userform.save()
            user.set_password(user.password)
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
            user = userform.save()
            user.set_password(user.password)
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
           
            if is_admin(user):
                return redirect('admindashboard')
            elif is_patient(user):
                return HttpResponse('<H1>PATIENT DASHBOARD</h1>')
            elif is_doctor(user):
                return HttpResponse('<h1>DOCTOR DASHBOARD</h1>')
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
          
            if user.groups.filter(name='PATIENT').exists():
                approvel = Patient.objects.all().filter(user_id=request.user.id,status=True)
                if approvel:
                    return HttpResponse('<H1>PATIENT DASHBOARD</h1>')
                else:
                    messages.warning(request,'Wait For Approvel')

            
    return render(request,'hospital/patientLogin.html')

@login_required(login_url='adminlogin')
def ViewAdminDashboard(request):
    # Doctor 
    doctors = Doctor.objects.all()
    doctorNum = Doctor.objects.all().count()
    # Patient 
    patients= Patient.objects.all()
    patientNum = Patient.objects.all().count()
    return render(request,'hospital/adminDashboard.html',locals())

@login_required(login_url='adminlogin')
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
def ViewAdmindDoctor(request):
    doctors = Doctor.objects.all().filter(status=True)
    return render(request,'hospital/adminDoctor.html',locals())
@login_required(login_url='adminlogin')

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
def ViewAdminDoctorDelete(request,id):
    doctor = Doctor.objects.get(user_id=id)
    user = User.objects.get(id=id)
    user.delete()
    doctor.delete()
    
    return redirect('admindashboardDoctor ')




@login_required(login_url='adminlogin')
def ViewAdminDashboardAppointment(request):
    
    return render(request,'hospital/adminAppointment.html')

@login_required(login_url='adminlogin')
def ViewAdminDashboardPatient(request):

    return render(request,'hospital/adminDashboardPatient.html')

@login_required(login_url='adminlogin')
def ViewAdminDashboardDoctor(request):

    return render(request,'hospital/adminDashboardDoctor.html')

@login_required(login_url='adminlogin')
def ViewAdmindPatient(request):
    patients = Patient.objects.all().filter(status=True)
    print(patients)
    return render(request,'hospital/adminPatient.html',locals())
    
@login_required(login_url='adminlogin')
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
def ViewAdmindDoctorApprove(request):
    doctors = Doctor.objects.all().filter(status=False)
    return render(request,'hospital/adminApproveDoctor.html',locals())

@login_required(login_url='adminlogin')
def ViewDoctorApprove(request,id):
    doctors = Doctor.objects.get(id=id)
    doctors.status=True
    doctors.save()
    print(doctors)
    return redirect('adminDoctor')

@login_required(login_url='adminlogin')
def ViewDoctorReject(request,id):
    doctor = Doctor.objects.get(id=id)
    user = User.objects.get(id=doctor.user_id)
    doctor.delete()
    user.delete()
    return redirect('adminDoctor')


@login_required(login_url='adminlogin')
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
def ViewAdminPatientApprovevel(request):
    patients = Patient.objects.all().filter(status=False)
    return render(request,'hospital/patientApprovel.html',locals())

@login_required(login_url='adminlogin')
def ViewAdminPatientApprove(request,id):
    patient = Patient.objects.get(id=id)
    patient.status = True
    patient.save()
    return redirect('adminPatient')

@login_required(login_url='adminlogin')
def ViewAdminPatientReject(request,id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    patient.delete()
    user.delete()
    return redirect('adminPatient')

@login_required(login_url='adminlogin')
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
def ViewAdminPatientDelete(request,id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    patient.delete()
    user.delete()
    messages.warning(request,'Patient Remove Succesfully')
    return redirect('adminPatient')

@login_required(login_url='adminlogin')
def ViewAdminAddAppointment(request):
    frm_unbound = AppointmentForm()
    
    if request.method == 'POST':
        frm_bound = AppointmentForm(request.POST)
        print('enter ')
        if frm_bound.is_valid():
            print('success')
            appointment  = frm_bound.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = User.objects.get(id=request.POST.get('patientId')).first_name
            # appointment.status  = True
            appointment.save()
            messages.success(request,'Appointment Add Successfully ')
            return redirect('admindashboardApppintment')
        else:
            print('errors')
        
    return render(request,'hospital/adminAddAppointment.html',{'appointment':frm_unbound})

@login_required(login_url='adminlogin')
def ViewAdminViewAppointment(request):
    appointment = Appointment.objects.all().filter(status=True)
    return render(request,'hospital/adminViewAppointment.html',locals())


@login_required(login_url='adminlogin')
def ViewAdminApprovelAppointment(request):
    appointment = Appointment.objects.all().filter(status=False)
    return render(request,'hospital/adminApprovelAppointment.html',locals())

@login_required(login_url='adminlogin')
def ViewAdminApproveAppointment(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = True
    appointment.save()
    print('approve')
    return redirect('adminViewAppointment')

@login_required(login_url='adminlogin')
def ViewAdminRejectAppointment(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    print('delete')
    return redirect('adminViewAppointment')


@login_required(login_url='adminlogin')
def ViewAdminPatientDischarge(request):
    patients = Patient.objects.all().filter(status=True)
    return render(request,'hospital/adminDischargePatient.html',locals())


class GallaryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallarySerialzers

def ShowAllImages(request):
    images = Gallery.objects.all()
    return render(request,'hospital/showAllImages.html',locals())