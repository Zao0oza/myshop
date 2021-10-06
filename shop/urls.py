from django.urls import path

from .views import *

urlpatterns=[
    path('', RecentGoods.as_view(), name='home'),
    path('feedback/', feedback, name='feedback'),
    path('products/', ProductsPage.as_view(), name='products'),
    path('<slug>/', AboutPage.as_view(), name='about'),
    path('contact/', ContactPage.as_view(), name='contact'),
    path('feedback/', feedback, name='feedback'),

]