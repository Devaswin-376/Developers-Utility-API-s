from django.urls import path
from .views import BarcodeGenerateView, BarcodeListView, BarcodeDetailView,BarcodeDeleteView, BarcodeDownloadView

urlpatterns = [
    path('generate/', BarcodeGenerateView.as_view(), name='barcode-generate'),
    path('list/', BarcodeListView.as_view(), name='barcode-list'),
    path('<int:id>/', BarcodeDetailView.as_view(), name='barcode-detail'),
    path('delete/<int:id>/', BarcodeDeleteView.as_view(), name='barcode-delete'),
    path('download/<int:id>/', BarcodeDownloadView.as_view(), name='barcode-download'),
]
