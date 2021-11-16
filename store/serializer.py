from .models import Collection
from django.db.models.query import QuerySet
from rest_framework import fields, serializers
from decimal import Decimal

from store.models import Product

from store import models


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','slug','description','inventory','unit_price','tax','collection']
   
   
    tax=serializers.SerializerMethodField(method_name='tax_calc')
   
   
    def tax_calc(self,product:Product):
        return product.unit_price*Decimal(1.1)

    '''normal representation of the serializer'''
    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
    # price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    
    # collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-details'
    # )

    