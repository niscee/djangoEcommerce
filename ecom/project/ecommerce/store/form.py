from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Profile, Category, SiteInfo, CustomOrder, CustomerContactManager

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
        fields = ['category','name','special','detail','price','image','stock']  


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['c_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','phone']  

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username']


class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = ['about','logo'] 


class CustomOrderForm(forms.ModelForm):
    date = forms.DateField()
    class Meta:
        model = CustomOrder
        widgets = {
            'date': forms.TextInput(attrs={'placeholder': 'format: 2019-12-16'})
        }
        fields = ['size', 'date', 'extra_items', 'custom_details', 'materials'] 


class ContactManagerForm(forms.ModelForm):
    class Meta:
        model = CustomerContactManager
        fields = ['messages']
                      






               