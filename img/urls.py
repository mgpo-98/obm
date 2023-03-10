from django.urls import path
from . import views


app_name = 'img'

urlpatterns =[
    path('',vies.index, name='index'),
]