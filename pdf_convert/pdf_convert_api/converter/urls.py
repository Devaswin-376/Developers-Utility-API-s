# converter/urls.py
from django.urls import path
from .views import ImageToPDFView, HTMLToPDFView, ConversionListView

urlpatterns = [
    path('image-to-pdf/', ImageToPDFView.as_view(), name='image-to-pdf'),
    path('html-to-pdf/', HTMLToPDFView.as_view(), name='html-to-pdf'),
    path('list/', ConversionListView.as_view(), name='conversion-list'),
]
