from rest_framework import generics, status 
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import UploadedFile
from .serializers import UploadedFileSerializer 

# Create your views here.
class FileUploadView(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provied"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = UploadedFile.objects.create(
            file=file_obj,
            file_name=file_obj.name,
            file_type=file_obj.content_type,
            file_size=file_obj.size,
        )

        serializer = self.get_serializer(uploaded_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# List all files
class FileListView(generics.ListAPIView):
    queryset = UploadedFile.objects.all().order_by('-uploaded_at')
    serializer_class = UploadedFileSerializer

# Retrieve a single file
class FileDetailView(generics.RetrieveAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    lookup_field = 'id'

# Delete a file
class FileDeleteView(generics.DestroyAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        file_instance = get_object_or_404(UploadedFile, id=kwargs['id'])
        file_instance.file.delete(save=False)  # Delete file from storage
        file_instance.delete()
        return Response({"message": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT)