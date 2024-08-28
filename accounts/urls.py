from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns =[
   path('signup',views.signup, name='signup'),
   path('check-nickname/', views.check_nickname, name='check_nickname'),
   path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
]