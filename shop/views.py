from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import F

from cart.forms import CartAddProductForm
from shop.forms import ContactForm
from shop.models import *
from django.contrib import messages


def about(request):
    return render(request, 'shop/about.html')


class ContactPage(DetailView):
    model = ContentFor
    template_name = 'shop/about.html'
    context_object_name = 'сontentfor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ОБО МНЕ'
        return context


class ProductsPage(ListView):
    model = Products
    template_name = 'shop/products.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self,**kwargs):
        queryset=super().get_queryset(**kwargs)
        if self.request.method == 'GET':
            if 'low' in self.request.GET:
                return queryset.order_by('price')
            elif 'high' in self.request.GET:
                return queryset.order_by('-price')
            elif 'new' in self.request.GET:
                return queryset.order_by('-created_at')
            elif 'all' in self.request.GET:
                return queryset
            else:
                return queryset

        else:
            return queryset


class RecentProducts(ListView):
    model = Products
    template_name = 'shop/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Products.objects.order_by('-created_at')[:6]


def feedback(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['email']+'\n'+ form.cleaned_data['content'], 'danfeigin@yandex.ru', ['sefeigin@mail.ru'], fail_silently=False)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки')
    else:
        form = ContactForm()
    return render(request, 'shop/feedback.html', {'form': form})


class GetProduct(DetailView):
    model = Products
    template_name = 'shop/single-product.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


def product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug)
    cart_product_form=CartAddProductForm()
    return render(request, 'shop/single-product.html', {'post': product,                                       'cart_product_form': cart_product_form})