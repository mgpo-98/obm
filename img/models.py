from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import  ProcessedImageField
# Create your models here.
import os

class Review(models.Model):
    image = ProcessedImageField(upload_to='img/zzal', blank=True,
                            processors=[ResizeToFill(1200, 960)],
                            format='JPEG',
                            options={'quality': 80})
    