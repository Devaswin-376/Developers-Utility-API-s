from rest_framework import serializers
from .models import IPRecord

class IPRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPRecord
        fields = '__all__'
