from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models

class SignUpForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=10)
    college_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile_number', 'college_name', 'password1', 'password2')
