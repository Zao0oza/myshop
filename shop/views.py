
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.views.generic import ListView, DetailView


from cart.cart import Cart
from cart.forms import CartAddProductForm
from shop.forms import ContactForm
from shop.models import *
from django.contrib import messages
from .forms import NewUserForm, OrderCreateForm
from django.contrib.auth import login, authenticate, logout


def about(request):
    return render(request, 'shop/about.html')


class ProductsPage(ListView):# класс отвечающий за страницу отображающие все товары
    model = Products
    template_name = 'shop/products.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self, **kwargs):# отвечает за фильтрации товаров по цене и дате добавления, принимает название кнопки методом get и сортирует исходя из него
        queryset = super().get_queryset(**kwargs).filter(is_published=True)
        if self.request.method == 'GET':
            try:
                return queryset.order_by(list(self.request.GET.items())[1][0])# сортирует по названию кнопки !!! Исключение ошибки длины списка когда страница тольк прогрузилась
            except:
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
    form = CartAddProductForm()
    product = get_object_or_404(Products, slug=slug)
    cart = Cart(request)
    if request.method == "POST":
        form = CartAddProductForm(request.POST, )
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
            return redirect('cart:cart_detail')
    return render(request, 'shop/single-product.html',
                  {'post': product, 'form': form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("home")
        messages.error(request, "Ошибка. Проверьте указанные данные")
    form = NewUserForm()
    return render(request=request, template_name="shop/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if request.session:
                print(request.session['cart'])
            else:
                pass
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Добро пожаловать {username}.")
                return redirect("home")
            else:
                messages.error(request, "Неправильный пароль.")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="shop/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из аккаунта.")
    return redirect("home")


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart_template=cart.save()
            cart.clear()
            return render(request, 'shop/order_created.html',
                          {'order': order, 'cart': cart_template})
    else:
        form = OrderCreateForm
    return render(request, 'shop/order_create.html',
                  {'cart': cart, 'form': form})


class GetUserOrders(ListView):
    model = Orders
    template_name = 'shop/user_orders.html'
    context_object_name = 'orders'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Orders.objects.all().filter(user=self.request.user).order_by('-order_completed', 'ordered_at')


class OrderDetailed(DetailView):
    model = Orders
    template_name = 'shop/order_detailed.html'
    context_object_name = 'order'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказ'
        return context
