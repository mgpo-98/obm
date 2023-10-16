from django.urls import path
from . import views


app_name = 'img'

urlpatterns =[
    path('',views.index, name='index'),
    path("image_list", views.image_list, name="image_list"),
]