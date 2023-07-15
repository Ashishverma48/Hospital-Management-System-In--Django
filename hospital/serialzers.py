from rest_framework import serializers
from .models import *
class GallarySerialzers(serializers.ModelSerializer):
    class Meta:
          model = Gallery
          fields = '__all__'