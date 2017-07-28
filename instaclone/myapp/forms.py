from django import forms
from models import UserModel, post


class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'name', 'email', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['image', 'caption']