from django.db import models
from django.contrib.auth.models import User
# Create your models here.
departments = [('Cardiologist', 'Cardiologist'),
               ('Dermatologists', 'Dermatologists'),
               ('Emergency Medicine Specialists',
                'Emergency Medicine Specialists'),
               ('Allergists/Immunologists', 'Allergists/Immunologists'),
               ('Anesthesiologists', 'Anesthesiologists'),
               ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
               ]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(
        max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name},{self.department}"
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

class PatientManager(models.Manager):
    def search_by_first_name(self, first_name):
        return self.get_queryset().filter(user__first_name__icontains=first_name)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)


    objects = PatientManager()

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.user.first_name},{self.symptoms}"


class Appointment(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.patientName


class Gallery(models.Model):
    categories = [('Cardiology', 'Cardiology'),
                ('Dental', 'Dental'),

                ('Neurology', 'Neurology'),
                ('Laboraty', 'Laboraty'),
                ]
    category=models.CharField(choices=categories,max_length=50,default='Cardiologist')
    images  = models.ImageField(upload_to='gallary/')

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email =models.EmailField()
    MobileNo=models.CharField(max_length=15)
    message  = models.TextField()

    def __str__(self):
        return self.name


    
