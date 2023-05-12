from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Payment_Account


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Payment_Account
        fields = ('username', 'name', 'user_id_number', 'user_phone', 'password')
