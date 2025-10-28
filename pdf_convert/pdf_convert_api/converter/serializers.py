from rest_framework import serializers
from .models import Conversion

class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = '__all__'
        read_only_fields = ['output_pdf', 'created_at']