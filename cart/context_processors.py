from .cart import Cart

# Контекстный процессор для корзины
def cart(request):
    return{'cart': Cart(request)}