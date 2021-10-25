from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import F
from django.db.models import Count

from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.forms import ContactForm
from shop.models import *
from django.contrib import messages
from .forms import NewUserForm, OrderCreateForm
from django.contrib.auth import login, authenticate, logout


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

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
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
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['email'] + '\n' + form.cleaned_data['content'], 'danfeigin@yandex.ru',
                             ['sefeigin@mail.ru'], fail_silently=False)
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
    cart_product_form = CartAddProductForm()
    product_tags_ids = Products.tags.values_list('id', flat=True)
    similar_product = Products.objects.filter(tags__in=product_tags_ids).exclude(id=product.id)
    similar_product = similar_product.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    return render(request, 'shop/single-product.html',
                  {'post': product, 'cart_product_form': cart_product_form, 'similar_posts': similar_product})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="shop/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if  request.session:
                print(request.session['cart'])
            else:
                pass
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="shop/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'shop/order_created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'shop/order_create.html',
                  {'cart': cart, 'form': form})