from django import forms
from django.forms.widgets import ClearableFileInput

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'gif', 'hashtags']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
            'gif': ClearableFileInput(attrs={'multiple': True}),
        }
