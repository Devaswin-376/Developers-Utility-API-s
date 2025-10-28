import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import IPRecord
from .serializers import IPRecordSerializer


class IPLookupView(APIView):
    def post(self, request):
        ip = request.data.get("ip")
        if not ip:
            return Response({"error": "IP address required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Call external API
        url = f"https://ipapi.co/{ip}/json/"
        res = requests.get(url)
        data = res.json()

        if 'error' in data:
            return Response({"error": "Invalid IP or lookup failed"}, status=status.HTTP_400_BAD_REQUEST)

        record = IPRecord.objects.create(
            ip_address=data.get("ip", ""),
            city=data.get("city", ""),
            region=data.get("region", ""),
            country=data.get("country_name", ""),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            timezone=data.get("timezone", "")
        )

        serializer = IPRecordSerializer(record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class MyIPView(APIView):
    def get(self, request):
        res = requests.get("https://ipapi.co/json/")
        data = res.json()
        return Response(data)



class IPListView(generics.ListAPIView):
    queryset = IPRecord.objects.all().order_by('-created_at')
    serializer_class = IPRecordSerializer



class IPDeleteView(APIView):
    def delete(self, request, id):
        record = get_object_or_404(IPRecord, id=id)
        record.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
