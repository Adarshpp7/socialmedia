from django import forms
from django.contrib.auth.models import User
from .models import User_Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'm-1'}))
    # bio = forms.CharField(max_length=300)
    # gender = forms.CharField(max_length=10)


    class Meta:
        model = User_Profile
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2')

class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'm-2'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'm-2'}))
         
           
    
      


