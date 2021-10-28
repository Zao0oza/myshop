from django import template
from shop.models import OrderItem


register = template.Library()

@register.simple_tag()
def show_orderitem(order_id):
      return OrderItem.objects.filter(order_id=order_id)

