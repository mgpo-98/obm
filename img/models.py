from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True) # 다수의 해시태그를 저장하는 필드
    download_count = models.IntegerField(default=0)
    def __str__(self):
        return f"이미지 {self.id} - 다운로드 횟수: {self.download_count}"

    
class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)
    daily_rank = models.IntegerField(default=0)
    weekly_rank = models.IntegerField(default=0)
    overall_rank = models.IntegerField(default=0)
    def __str__(self):
        return self.query