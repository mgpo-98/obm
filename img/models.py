from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    tags  = models.ManyToManyField('Hashtag', blank=True) # 다수의 해시태그를 저장하는 필드
    
class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
