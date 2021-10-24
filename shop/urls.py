from django.urls import path

from .views import *

urlpatterns=[
    path('', RecentProducts.as_view(), name='home'),
    path('feedback/', feedback, name='feedback'),
    path('products/', ProductsPage.as_view(), name='products'),
    path('about/', about, name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('products/<str:slug>/', product_detail, name='product'),
    path("register", register_request, name="register"),

]