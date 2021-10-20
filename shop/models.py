from debug_toolbar import forms
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.urls import reverse, reverse_lazy


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тэг')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']



class Products(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    amount = models.IntegerField(verbose_name='Кол-во')
    price = MoneyField(default=0, max_digits=14, decimal_places=0, default_currency='RUB', verbose_name='Цена')
    tags = models.ManyToManyField(Tag, blank=True, related_name='product')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})


class ContentFor(models.Model): #класс создан для удобного заполнения страницы обо мне контентом через ckeditor, запрос по slug
    title = models.CharField(max_length=50, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)#

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('сontentfor', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['title']


class ImagesInline (models.Model):
    products = models.ForeignKey(Products, default=None, on_delete=models.PROTECT, related_name='image')
    image = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)