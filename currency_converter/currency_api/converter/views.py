# converter/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrencyConverterSerializer

# Example static rates w.r.t USD
RATES = {
    "USD": 1,
    "INR": 83.3,
    "EUR": 0.91,
    "GBP": 0.78,
    "JPY": 150.0,
    "AUD": 1.53,
    "CAD": 1.33
}

class CurrencyConvertView(APIView):
    def post(self, request):
        serializer = CurrencyConverterSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            from_currency = serializer.validated_data['from_currency'].upper()
            to_currency = serializer.validated_data['to_currency'].upper()

            if from_currency not in RATES or to_currency not in RATES:
                return Response({"error": "Currency not supported."}, status=status.HTTP_400_BAD_REQUEST)

            # Convert via USD as base
            usd_amount = amount / RATES[from_currency]
            converted_amount = usd_amount * RATES[to_currency]

            return Response({
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "converted_amount": round(converted_amount, 2)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
