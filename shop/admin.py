from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import *
from django import forms


class GoodsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Goods
        fields = '__all__'


class ContentForAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = ContentFor
        fields = '__all__'


class GoodsAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    form = GoodsAdminForm
    list_display = ('id', 'name', 'slug', 'price', 'amount',  'category', 'created_at', 'get_photo', )
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('category',)
    readonly_fields = ('created_at', 'get_photo')
    fields = ('name', 'slug', 'category', 'price','amount',  'tags', 'description', 'photo', 'get_photo', 'created_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'фото'


class ContentForAdmin(admin.ModelAdmin):
    form = ContentForAdminForm
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'slug', )
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    fields = ('title', 'slug', 'content')



class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ContentFor, ContentForAdmin)