from django.db import models

# Create your models here.
import os

class Document(models.Model):
    attached = models.FileField('첨부 파일', upload_to='img/zzal')

    def get_filename(self):
        return os.path.basename(self.attached.name)