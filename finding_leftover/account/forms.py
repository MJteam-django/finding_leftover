
from django.contrib.auth.models import User
from django import forms
from post.models import Store
from django import forms
from django.forms import ModelForm

from django.db import models
from betterforms.multiform import MultiModelForm
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'password1' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '사용자ID',
            'password1': 'Password',
            'password2': 'Password 확인',
        }
        
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('store_name', 'store_adress', 'store_memo')
        widgets = {
            'store_name': forms.TextInput(attrs={'class': 'form-control'}),
            'store_adress': forms.TextInput(attrs={'class': 'form-control'}),
            'store_memo': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'store_name': '가게이름',
            'store_adress': '가게주소',
            'store_memo': '가게 소개',
        }

class UserCreationMultiForm(MultiModelForm):
    form_classes={
        'user' : CreateUserForm,
        'store' : StoreForm,
    }

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']