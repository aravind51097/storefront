from .models import Collection, Reviews
from rest_framework import fields, serializers
from decimal import Decimal

from store.models import Product

from store import models


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','product_count']
    product_count=serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','slug','description','inventory','unit_price','tax','collection']
   
   
    tax=serializers.SerializerMethodField(method_name='tax_calc')
   
   
    def tax_calc(self,product:Product):
        return product.unit_price*Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reviews
        fields=['id','date','name','description',]

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Reviews.objects.create(product_id=product_id,**validated_data)
    