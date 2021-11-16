from rest_framework import serializers
from decimal import Decimal

from store.models import Product


class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    tax=serializers.SerializerMethodField(method_name='tax_calc')


    def tax_calc(self,product:Product):
        return product.unit_price*Decimal(1.1)