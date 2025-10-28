from rest_framework import serializers

class CurrencyConverterSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    from_currency = serializers.CharField(max_length=10)
    to_currency = serializers.CharField(max_length=10)
