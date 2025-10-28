import os
import barcode
from barcode.writer import ImageWriter
from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Barcode
from .serializers import BarcodeSerializer

class BarcodeGenerateView(generics.CreateAPIView):
    serializer_class = BarcodeSerializer

    def post(self, request):
        data = request.data.get("data")

        if not data:
            return Response({"error": "Data field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate barcode
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(data, writer=ImageWriter())

        # Define file path
        file_name = f"{data}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, "barcodes", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the barcode image
        barcode_instance.save(file_path[:-4])  # remove ".png" because save() adds it automatically

        # Store in DB
        barcode_record = Barcode.objects.create(
            data=data,
            image=f"barcodes/{file_name}"
        )

        serializer = self.get_serializer(barcode_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BarcodeListView(generics.ListAPIView):
    queryset = Barcode.objects.all().order_by('-created_at')
    serializer_class = BarcodeSerializer


class BarcodeDetailView(generics.RetrieveAPIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    lookup_field = 'id'
    

class BarcodeDeleteView(generics.DestroyAPIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        barcode_instance = get_object_or_404(Barcode, id=kwargs['id'])
        # Delete the image file from media folder
        if barcode_instance.image:
            barcode_instance.image.delete(save=False)
        barcode_instance.delete()
        return Response({"message": "Barcode deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class BarcodeDownloadView(generics.RetrieveAPIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        barcode_instance = get_object_or_404(Barcode, id=kwargs['id'])
        file_path = barcode_instance.image.path
        
        try:
            #Opens file in binary mode
            file_handle = open(file_path, 'rb')
            response = FileResponse(file_handle, content_type='image/png')
            response['Content-Disposition'] = f'attachment: filename="{barcode_instance.data}.png"'
            return response
        except FileNotFoundError:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
