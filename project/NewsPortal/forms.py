from typing import Type

import requests
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, User
from django.contrib.auth.views import PasswordChangeForm, AuthenticationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostFormCreate_and_Update(forms.ModelForm):
    class Meta:
        model = Post
        labels = {'author': 'Автор',
                  'article': 'Тип',
                  'category': 'Категория',
                  'heading': 'Заголовок',
                  'text': 'Тест',
                  }
        fields = ['author', 'article', 'category', 'heading', 'text']


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        labels = {'username': 'Логин',
                  'first_name': 'Имя',
                  'last_name': 'Фамилия',
                  'email': 'E-mail'}
        fields = ['first_name', 'last_name', 'email', 'username']
        help_texts = {'username': ' '}


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Повторите новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'})),
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        g = Group.objects.get(name='Authors')
        g.user_set.add(user)
        return user


