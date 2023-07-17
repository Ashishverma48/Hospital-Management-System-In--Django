from django import forms
from django.contrib.auth.models import User
from .models import *


class AdminForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        labels={'first_name':'First Name','last_name':'Last Name','username':'Username','email':'Email'}
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=f'Enter {frm.label}'

   
 
class DoctorUserForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        labels={'first_name':'First Name','last_name':'Last Name','username':'Username','email':'Email'}
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=f'Enter {frm.label}'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields =['address','mobile','department','profile_pic']
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=f'Enter {frm.label}'
    
 
class PatientUserForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        labels={'first_name':'First Name','last_name':'Last Name','username':'Username','email':'Email'}
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=f'Enter {frm.label}'

class PatientForm(forms.ModelForm):
    assignedDoctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model = Patient
        fields =['address','mobile','symptoms','profile_pic']
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=f'Enter {frm.label}'
    

   
 
class AppointmentForm(forms.ModelForm):
    patientId = forms.ModelChoiceField(queryset=Patient.objects.all().filter(status=True),empty_label='Patient Name And Symptoms',to_field_name='user_id')
    doctorId = forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label='Doctor Name And Department',to_field_name='user_id')
    class Meta:
        model = Appointment
        fields = ['description']
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=frm.label

 
class PatientAppointmentForm(forms.ModelForm):
    
    doctorId = forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label='Doctor Name And Department',to_field_name='user_id')
    class Meta:
        model = Appointment
        fields = ['description']
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=frm.label



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','MobileNo','message']
        labels={'name':'Enter Name','email':'Enter Email','MobileNo':'Mobile Number','message':'Enter Message'}

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['placeholder'] = f'Enter {frm.label}'
            frm.widget.attrs['class'] = 'form-control'

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'
