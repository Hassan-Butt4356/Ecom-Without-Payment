from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address


class CreateUser(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {'st_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 Main St'})}
