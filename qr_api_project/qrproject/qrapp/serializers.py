from rest_framework import serializers
from .models import QRCode

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'data', 'image','color','background' ,'created_at']
        read_only_fields = ['id', 'image', 'created_at']
