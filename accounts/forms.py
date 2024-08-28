# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email_local = forms.CharField(label="Email", max_length=100)
    email_domain = forms.CharField(max_length=100, required=False)
    nickname = forms.CharField(label="Nickname", max_length=30)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'email', 'nickname')

    def clean(self):
        cleaned_data = super().clean()
        email_local = cleaned_data.get('email_local')
        email_domain = cleaned_data.get('email_domain')
        
        if email_local and email_domain:
            cleaned_data['email'] = f"{email_local}@{email_domain}"

        return cleaned_data
