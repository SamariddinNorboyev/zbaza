from django.contrib.auth import authenticate, login
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        if not user:
            raise ValidationError('Username yoki Password xato!')
        return cleaned_data