from django import template
from shop.models import OrderItem, Orders

register = template.Library()


@register.simple_tag()
def show_orderitem(order_id):
    return OrderItem.objects.filter(order_id=order_id)


@register.inclusion_tag('shop/orders_tpl.html')
def show_orders(status=True):
    return Orders.objects.filter(order_completed=status)
