from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import F

from shop.forms import ContactForm
from shop.models import *
from django.contrib import messages




class AboutPage(DetailView):
    model = ContentFor
    template_name = 'shop/about.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ОБО МНЕ'
        return context


class ContactPage(DetailView):
    model = ContentFor
    template_name = 'shop/about.html'
    context_object_name = 'сontentfor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ОБО МНЕ'
        return context


class ProductsPage(ListView):
    model = Goods
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


class RecentGoods(ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Goods.objects.order_by('-created_at')[:6]


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
    model = Goods
    template_name = 'shop/single-product.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        self.object.views = F('views')+1
        self.object.save()
        self.object.refresh_from_db()
        return context
