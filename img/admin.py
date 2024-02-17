from django.contrib import admin
from .models import Image, Hashtag, SearchHistory  # assuming admin.py is in the same app directory

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'download_count']
    actions = ['delete_selected']

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    actions = ['delete_selected']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'query', 'search_time', 'daily_rank', 'weekly_rank', 'overall_rank']
    actions = ['delete_selected']
