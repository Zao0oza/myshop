from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from django.contrib import admin
from django.contrib.auth.models import User

from .models import Orders


class OrderCreateForm(forms.ModelForm):  # форма заказа
    class Meta:
        model = Orders
        fields = ['first_name', 'last_name', 'email', 'address', 'zip_code', 'city', 'phone_number', 'user']
        widgets = {
            'user': forms.HiddenInput(),  # используется для того чтобы если пользователь авторизован сохранять его имя
            # в заказе
        }

    def __init__(self, *args, **kwargs):  # добавляет всем полям виджета класс для взаимодействия с css
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        for field in self:
            field.field.widget.attrs['class'] = "form-control"


class ContactForm(forms.Form):  # форма обратной связи
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


class NewUserForm(UserCreationForm):# форма регистрации поллзователя
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
