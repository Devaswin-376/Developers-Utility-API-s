import random, string
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics,status
from rest_framework.response import Response
from .models import ShortURL
from .serializers import ShortURLSerializer

def generate_short_code():
    #Generate a random 6-character aplhanumeric short url code
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenURLView(generics.CreateAPIView):
    serializer_class = ShortURLSerializer

    def post(self, request):
        original_url = request.data.get("original_url")
        if not original_url:
            return Response({"error": "original_url is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        #generate a unique code
        short_code = generate_short_code()
        while ShortURL.objects.filter(short_code=short_code).exists():
            short_code = generate_short_code()
        
        short_instance = ShortURL.objects.create( original_url=original_url, short_code=short_code)
        
        
        short_url = f"http://127.0.0.1:8000/api/short/{short_code}/"
        data = {
            "id": short_instance.id,
            "original_url": original_url,
            "short_code": short_code,
            "short_url": short_url,
            "created_at": short_instance.created_at
        }
        
        return Response(data, status=status.HTTP_201_CREATED)

class URLListView(generics.ListAPIView):
    queryset = ShortURL.objects.all().order_by('-created_at')
    serializer_class = ShortURLSerializer
    
class RedirectView(generics.RetrieveAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'short_code'
    
    def get(self, request, *args, **kwargs):
        short_instance = get_object_or_404(ShortURL, short_code=kwargs['short_code'])
        return redirect(short_instance.original_url)
    
class DeleteShortURLView(generics.DestroyAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(ShortURL, id=kwargs['id'])
        instance.delete()
        return Response({"message": "Short URL deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
