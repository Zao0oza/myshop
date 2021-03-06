from django.urls import path

from .views import *

urlpatterns=[
    path('', RecentProducts.as_view(), name='home'),
    path('feedback/', feedback, name='feedback'),
    path('products/', ProductsPage.as_view(), name='products'),
    path('about/', about, name='about'),
    path('products/<str:slug>/', product_detail, name='product'),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name= "logout"),
    path('create/', order_create, name='order_create'),
    path('account/orders/', GetUserOrders.as_view(), name='orders_list'),
    path('account/order/<int:pk>/', OrderDetailed.as_view(), name='order_detail'),

]