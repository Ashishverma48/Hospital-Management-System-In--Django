from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def viewHome(request):
    return render(request,'hospital/index.html')

def ViewLogin(request):
    return render(request,'hospital/login.html')


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





def ViewAdminLogin(request):
    if request.method == 'POST':

        username = request.POST.get('adminUserName')
        password = request.POST.get('adminPassword')
        print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.groups.filter(name='ADMIN').exists():
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
            login(request,user)
           
            if user.groups.filter(name='DOCTOR').exists():
                return HttpResponse('<h1>DOCTOR DASHBOARD</h1>')
            if user.groups.filter(name="PATIENT").exists():
                return HttpResponse('<H1>PATIENT DASHBOARD</h1>')
            if user.groups.filter(name="ADMIN").exists():
                return redirect('admindashboard')
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
                return HttpResponse('<H1>PATIENT DASHBOARD</h1>')
            
    return render(request,'hospital/patientLogin.html')

def ViewAdminDashboard(request):
    # Doctor 
    doctors = Doctor.objects.all()
    doctorNum = Doctor.objects.all().count()
    # Patient 
    patients= Patient.objects.all()
    patientNum = Patient.objects.all().count()
    return render(request,'hospital/adminDashboard.html',locals())

def ViewAdminDashboardMain(request):
    doctors = Doctor.objects.all()
    doctorNum = Doctor.objects.all().count()
    # Patient 
    print(doctors)

    patients= Patient.objects.all()
    patientNum = Patient.objects.all().count()
    return render(request,'hospital/adminDashboardMain.html',locals())

def ViewAdmindDoctor(request):
    doctors = Doctor.objects.all()
    return render(request,'hospital/adminDoctor.html',locals())
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
def ViewAdminDoctorDelete(request,id):
    doctor = Doctor.objects.get(user_id=id)
    user = User.objects.get(id=id)
    user.delete()
    doctor.delete()
    
    return redirect('admindashboardDoctor ')





def ViewAdminDashboardAppointment(request):
    
    return render(request,'hospital/adminAppointment.html')
def ViewAdminDashboardPatient(request):

    return render(request,'hospital/adminDashboardPatient.html')
def ViewAdminDashboardDoctor(request):

    return render(request,'hospital/adminDashboardDoctor.html')


def ViewAdmindPatient(request):
    patients = Patient.objects.all()
    print(patients)
    return render(request,'hospital/adminPatient.html',locals())