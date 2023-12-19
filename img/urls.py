from django.urls import path
from . import views


app_name = 'img'

urlpatterns =[
    path('',views.index, name='index'),
    path("image_list/", views.image_list, name='image_list'),
    path('search/', views.search_images, name='search_images'),  # 검색 결과 페이지
    path('download/<int:image_id>/', views.download_image, name='download_image'),
]