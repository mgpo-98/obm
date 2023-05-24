from django.db import models
from imagekit.processors import ResizeToFill

# Create your models here.
import os

class Document(models.Model):
    attached = models.FileField('첨부 파일', upload_to='img/zzal', blank=True,
                            processors=[ResizeToFill(1200, 960)],
                            format='JPEG',
                            options={'quality': 80})

    def get_filename(self):
        return os.path.basename(self.attached.name)