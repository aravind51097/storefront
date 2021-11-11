from typing import Counter
from django.contrib import admin,messages
from django.contrib.admin.decorators import action
from django.contrib.admin.options import TabularInline
from django.db.models.query import QuerySet
from . import models
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
# Register your models here.

#CUSTOMIZING THE filter
class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory_name'

    def lookups(self, request, model_admin):
        return [

            ('<10','low'),
            ('>10','high')  
                  ]
    def queryset(self, request , queryset:QuerySet):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)
        elif self.value()==">10":
            return queryset.filter(inventory__gt=10)

#CUSTOMER MODel
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    list_per_page=10
    ordering=['first_name','last_name']
    search_fields=['first_name__istartswith','last_name__istartswith']
#PRODUCT MODEL 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions=['inventory_clear']
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_filter=['collection','last_update',InventoryFilter]
    list_per_page=10
    list_select_related=['collection']
    search_fields=['product']

    
    @admin.display(ordering='title')
    def collection_title(self,Product):
        return Product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self,Product):
        if Product.inventory<10:
            return 'low'
        return 'Ok'
    
    @admin.action(description='clear inventory')
    def inventory_clear(self,request,queryset):
        update=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update} has been updated succefully',

        )

#COLLECTION MODEL
@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display=['title','product_count']
    list_per_page=10

    
    @admin.display(ordering='product')
    def product_count(self,collection):
        url=(reverse('admin:store_product_changelist')
        +'?'
        +urlencode(
            {
                'collection__id':str(collection.id)
            }
        )

        )
        return format_html("<a href='{}'>{}</a>",url,collection.product_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
         product_count=Count('product')
        )


#ORDER MODEL 
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    list_display=['id','placed_at','customer_name']
    list_select_related=['customer']
    

    def customer_name(self,Order):
        return Order.customer.first_name

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['product','quantity','unit_price']

