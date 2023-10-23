from django import forms
from .models import Image


class ImageUploadForm(forms.ModelForm):
    hashtags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '해시태그 입력 (#으로 시작)'}),
        label='해시태그'
    )

    class Meta:
        model = Image
        fields = ('image', 'hashtags')