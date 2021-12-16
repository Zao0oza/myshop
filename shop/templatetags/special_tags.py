from django import template
from shop.models import OrderItem, Tag, Products

register = template.Library()


@register.simple_tag() # возвращает состав заказа соответсвующий его id
def show_orderitem(order_id):
    return OrderItem.objects.filter(order_id=order_id)


@register.inclusion_tag('shop/tag_list_tpl.html')
def tags_list( products__id, cnt=5): # возвращает список товаров совподающих по тэгу
    tags = Tag.objects.filter(products__id = products__id)
    products=Products.objects.filter(tags__in= tags).exclude(id=products__id).distinct()[:cnt]
    return {'products': products}