import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework import generics, status
from rest_framework.response import Response
from .models import QRCode
from .serializers import QRCodeSerializer

class GenerateQRCodeView(generics.CreateAPIView):
    serializer_class = QRCodeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        color = request.data.get('color', 'black')
        background = request.data.get('background', 'white')
        
        if not data:
            return Response({"error": "Data field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate QR code with styling
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=color, back_color=background)
        
        #save to memory
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f"qr_{QRCode.objects.count() + 1}.png"

        qr_obj = QRCode(data=data, color=color, background=background)
        qr_obj.image.save(file_name, ContentFile(buffer.getvalue()), save=True)

        serializer = QRCodeSerializer(qr_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QRCodeListView(generics.ListAPIView):
    queryset = QRCode.objects.all().order_by('-created_at')
    serializer_class = QRCodeSerializer


class QRCodeDetailView(generics.RetrieveAPIView):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
