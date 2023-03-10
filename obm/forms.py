from django import forms
from .models import Img



class Img(forms.ModelForm):
    class Meta:
        model = Img
        fields = ['image']