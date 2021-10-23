from django import template
from shop.models import Products, Tag

register = template.Library()

@register.simple_tag
def get_products_list(tag='китай'):
    products_list=Products.objects.filter(tags__name=tag).distinct()
    return  products_list