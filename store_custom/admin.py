from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product 
from tags.models import TggedItems


class TagInline(GenericTabularInline):
    model=TggedItems
    autocomplete_fields=['tag']

class CustomProductAdmin(ProductAdmin):
    inlines=[TagInline] 


admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)