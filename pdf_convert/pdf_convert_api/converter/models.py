from django.db import models

# Create your models here.
class Conversion(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image to PDF'),
        ('html', 'HTML to PDF'),
    ]
    
    conversion_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    input_file = models.FileField(upload_to='uploads/input', blank=True, null=True)
    output_pdf = models.FileField(upload_to='uploads/output', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.conversion_type} - {self.id}"