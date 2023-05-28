from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    upload = forms.FileField(label='첨부 파일', required=False, 
          widget=forms.FileInput(attrs={'class': 'form'}))
    
    class Meta:
        model = Review
        fields = ['image']
        
