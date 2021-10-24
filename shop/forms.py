from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

from django.contrib import admin
from django.contrib.auth.models import User

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customer'


class ContactForm(forms.Form):

    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    inlines = (CustomerInline,)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 


