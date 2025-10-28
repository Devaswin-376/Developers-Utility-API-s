from django.urls import path
from .views import GenerateQRCodeView, QRCodeListView, QRCodeDetailView

urlpatterns = [
    path('generate/', GenerateQRCodeView.as_view(), name='qr-generate'),
    path('list/', QRCodeListView.as_view(), name='qr-list'),
    path('<int:pk>/', QRCodeDetailView.as_view(), name='qr-detail'),
]
