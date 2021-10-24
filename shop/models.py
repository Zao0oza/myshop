from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

from django.urls import reverse
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField


class Products(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    amount = models.PositiveSmallIntegerField(verbose_name='Кол-во', default=1)
    price = MoneyField(default=0, max_digits=14, decimal_places=0, default_currency='RUB', verbose_name='Цена')
    # tags = models.ManyToManyField(Tag, blank=True, related_name='product')
    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})


class ContentFor(
    models.Model):  # класс создан для удобного заполнения страницы обо мне контентом через ckeditor, запрос по slug
    title = models.CharField(max_length=50, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)  #

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('сontentfor', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['title']


class ImagesInline(models.Model):
    products = models.ForeignKey(Products, default=None, on_delete=models.PROTECT, related_name='image')
    image = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)


class CustomerAdress(models.Model):
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP", max_length=12)
    city = models.CharField("City", max_length=1024)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(verbose_name='Номер телефона')
    user_orders = models.ManyToManyField('Orders', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Orders(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_IN_DELIVERY ='in_delivery'
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Заказ в обработке'),
        (STATUS_IN_PROGRESS, 'Заказ подтвержден'),
        (STATUS_IN_DELIVERY, 'Передан службе доставки'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )


    product_name = models.ForeignKey(Products, default=None, on_delete=models.PROTECT)
    ordered_at = models.DateTimeField(auto_now=True, verbose_name='заказ создан')
    delivered_at = models.DateTimeField(verbose_name='доставлен', default=timezone.now, null=True, blank=True)
    payed = models.BooleanField(verbose_name='оплачен')
    customer = models.ForeignKey(Customer, default=None, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)

    def __str__(self):
        return str(self.id)



