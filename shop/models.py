from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


from django.urls import reverse
from djmoney.models.validators import MinMoneyValidator
from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField


class Products(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    amount = models.PositiveSmallIntegerField(verbose_name='Кол-во', default=1, )
    price = MoneyField(default=0, max_digits=14, decimal_places=0, default_currency='RUB', verbose_name='Цена',
                       validators=[MinMoneyValidator(0), ])
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


class ContentFor( models.Model):  # класс создан для удобного заполнения страницы обо мне контентом через ckeditor, запрос по slug
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


class Orders(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_IN_DELIVERY = 'in_delivery'
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Заказ в обработке'),
        (STATUS_IN_PROGRESS, 'Заказ подтвержден'),
        (STATUS_IN_DELIVERY, 'Передан в службу доставки'),
        (STATUS_COMPLETED, 'Заказ доставлен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    email = models.EmailField()
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField("Адрес", max_length=1024)
    zip_code = models.CharField("Почтовый индекс", max_length=20)
    tracking_number = models.CharField("Номер отслеживания", max_length=12, null=True, blank=True)
    city = models.CharField("Город", max_length=1024)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now=True, verbose_name='заказ создан')
    delivered_at = models.DateTimeField(verbose_name='доставлен', default=timezone.now, null=True, blank=True)
    payed = models.BooleanField(verbose_name='оплачен', default=False, null=True, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
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
    comment = models.TextField(max_length=255, verbose_name='Комментарий к заказу', null=True, blank=True)
    order_completed= models.BooleanField(default=0, verbose_name='Выполнен')# заказ активный или выполненный

    class Meta:
        ordering = ('-ordered_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return '{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + 300

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


