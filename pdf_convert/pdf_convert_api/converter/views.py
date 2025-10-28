from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from .models import Conversion
from .serializers import ConversionSerializer
from django.conf import settings
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from xhtml2pdf import pisa #used to convert HTML -> PDF
import os
from io import BytesIO

class ImageToPDFView(APIView):
    def post(self, request):
        file = request.FILES.get('image') #fetch image from request
        if not file:
            return Response({"error":"NO image uploaded."}, status=400)#returns if no image is found in the request
        
        #creating database record 
        conversion = Conversion.objects.create(conversion_type='image', input_file=file)
        image_path = conversion.input_file.path
        
        # Define output folder and PDF path
        output_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/output')
        os.makedirs(output_dir, exist_ok=True)  
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'uploads/output', f"{conversion.id}.pdf")
        
        # opens uploaded image using Pillow
        image = Image.open(image_path)
        
        # A4 page size in points (1 point = 1/72 inch)
        page_width, page_height = A4

        # Get image size
        img_width, img_height = image.size

        # Calculate aspect ratios
        aspect = img_width / img_height
        page_aspect = page_width / page_height

        # Scale the image to fit A4 while maintaining aspect ratio
        if aspect > page_aspect:
            # Image is wider than page
            new_width = page_width
            new_height = page_width / aspect
        else:
            # Image is taller than page
            new_height = page_height
            new_width = page_height * aspect

        # Calculate position to center the image
        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        
        #creating a PDF drawing canvas using ReportLab
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=A4)
        
        #creating pdf and save
        pdf_canvas.drawInlineImage(image_path, x, y, width=new_width, height=new_height)
        pdf_canvas.showPage()
        pdf_canvas.save()
        
        #saving converted pdf in database
        conversion.output_pdf.name = f"uploads/output/{conversion.id}.pdf"
        conversion.save()
        
        #returns after succesfull conversion
        return Response({
            "message": "Image converted to PDF successfully",
            "pdf_url": request.build_absolute_uri(conversion.output_pdf.url)
        }, status=201)
        
        
class HTMLToPDFView(APIView):
    def post(self, request):
        html_content = request.data.get('html') #extract HTML text.
        if not html_content:
            return Response({"error" :"No HTML content provided."}, status=400)#returns if no html data is given in request
        
        #creating databse record for pdf
        conversion = Conversion.objects.create(conversion_type='html')
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'uploads/output', f"{conversion.id}.pdf")
        
        #pdf creation 
        #w = write (create new file), b = binary mode 
        with open(pdf_path, "w+b") as pdf_file:
            pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest= pdf_file)
            
        #coverted pdf is stored in the path     
        conversion.output_pdf.name = f"uploads/output/{conversion.id}.pdf"
        conversion.save()
        
        #returns after successfull pdf conversion
        return Response({
            "message": "HTML converted to PDF successfully",
            "pdf_url": request.build_absolute_uri(conversion.output_pdf.url)
        }, status=201)
        
class ConversionListView(ListAPIView):
    queryset = Conversion.objects.all().order_by('-created_at')
    serializer_class = ConversionSerializer