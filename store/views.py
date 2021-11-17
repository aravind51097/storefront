
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Collection, Product
from .serializer import CollectionSerializer, ProductSerializer
from store import serializer


class ProductList(ListCreateAPIView):
   
    queryset= Product.objects.select_related('collection').all()
    serializer_class= ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}



class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def delete(self, request, pk):#ovveriding the delete method in RUD class
        product=get_object_or_404(Product,pk=pk)
        if product.orderitem_set.count()>0:
            return Response(
                {"error":'item cant be deleted cuz its ordered'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class=CollectionSerializer


class CollectionDetails(RetrieveUpdateDestroyAPIView):
    queryset=collection =Collection.objects.annotate(product_count=Count('products'))
    serializer_class=CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection,pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({'success':"product deleted "},status=status.HTTP_204_NO_CONTENT)
