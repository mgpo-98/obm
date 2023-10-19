from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    gif = models.ImageField(upload_to='media/', blank=True, null=True)
    tags = models.TextField(blank=True)

