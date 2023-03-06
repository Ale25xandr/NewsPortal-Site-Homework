from typing import Type

from django import forms
from .models import Post, User


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
                  'password': 'Пароль',
                  'email': 'E-mail'}
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        help_texts = {'username': ' '}
