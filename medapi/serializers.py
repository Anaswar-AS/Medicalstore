from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Medicine

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'quantity', 'price', 'user']
        read_only_fields = ['user']