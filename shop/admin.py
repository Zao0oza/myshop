from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import *
from django import forms


class ImageInline(admin.TabularInline):
    model = ImagesInline


class GoodsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Products
        fields = '__all__'


class GoodsAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    form = GoodsAdminForm
    list_display = ('id', 'name', 'slug', 'price', 'amount', 'created_at', 'get_photo', 'is_published',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'get_photo')
    fields = ('name', 'slug', 'price', 'amount', 'tags', 'description', 'photo', 'get_photo', 'created_at')
    list_editable = ('is_published',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'фото'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'ordered_at', 'delivered_at', 'payed', 'get_total_cost', 'order_completed')
    list_display_links = ('id',)
    list_editable = ('order_completed',)
    search_fields = ('product_name',)
    inlines = [OrderItemInline]
    list_filter = ('order_completed', 'payed')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Products, GoodsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
