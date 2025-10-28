from django.db import models
# Create your models here.

class QRCode(models.Model):
    data = models.TextField()  # text or URL or QR content
    image = models.ImageField(upload_to='qrcodes/')
    color = models.CharField(max_length=20, default='black')
    background = models.CharField(max_length=20, default='white')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR for {self.data[:30]}"
