from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password')