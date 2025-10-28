from rest_framework import serializers
from .models import Barcode

class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = '__all__'
