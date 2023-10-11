from django.db import models

# Create your models here.
class PdfAttachment(models.Model):
    pdf_file = models.FileField(max_length=100)