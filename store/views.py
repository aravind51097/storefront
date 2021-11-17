
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
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



'''
handling the exception in traditional way if objectt does not exist

@api_view()
def product_details(request,id):
    try:
        product=Product.objects.get(pk=id)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)'''

@api_view(['GET','PUT','DELETE'])
def product_details(request,id):
    product=get_object_or_404(Product,pk=id)#keeping the object outside for availablitiy on all bolcks
    if request.method=='GET':  
        
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
        if product.orderitem_set.count()>0:
            return Response(
                {"error":'item cant be deleted cuz its ordered'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(product_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            product_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
