from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Profile

# Create the form class.
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    class Meta:
        model = User
        fields = ['username','password'] 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','special','detail','price','image','stock']  


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','phone']  

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username']                     

               