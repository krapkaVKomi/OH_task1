from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class TestForm(forms.Form):
    test = forms.CharField(label='todoTaskPost', max_length=100)