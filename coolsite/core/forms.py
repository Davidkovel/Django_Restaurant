from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class BookTableForm(forms.ModelForm):
    table = forms.ModelChoiceField(queryset=BookTable.objects.filter(is_busy=0))

    class Meta:
        model = BookTable
        fields = ["table", "is_busy"]


class ContactForm(forms.ModelForm):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label="Описания отзива", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Contact  # Потом через Rest Api отображим Отзывы для клиента
        fields = ['name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        fields = ('username', 'email', 'password')
