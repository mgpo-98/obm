from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True) # 다수의 해시태그를 저장하는 필드
    
class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query