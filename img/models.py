from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import  ProcessedImageField
# Create your models here.
import os


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    gif = models.FileField(upload_to='post_gifs/', blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.content
