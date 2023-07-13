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
    class Meta:
        model = Patient
        fields =['address','mobile','symptoms','assignedDoctorId','profile_pic']
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for frm in self.fields.values():
            frm.widget.attrs['class']='form-control'
            frm.widget.attrs['placeholder']=f'Enter {frm.label}'
    

   
 