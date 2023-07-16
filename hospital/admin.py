from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
   list_display=['user','address','mobile','symptoms','assignedDoctorId','profile_pic']
        
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
   list_display=['user','address','mobile','department','profile_pic']
        
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
   list_display=['category',"images"]

@admin.register(Appointment)
class GalleryAdmin(admin.ModelAdmin):
   list_display=['patientId',"doctorId",'patientName','doctorName','description','appointmentDate','status']
        
