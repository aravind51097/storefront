import collections
from os import stat
from django.db.models.aggregates import Count
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.shortcuts import get_object_or_404
from rest_framework import serializers,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Collection, Product
from .serializer import CollectionSerializer, ProductSerializer



@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
        query_set=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(query_set,many=True,context={'request': request})
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

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
        


@api_view()
def collection_details(request,pk):
    collection=Collection.objects.get(pk=pk)
    serializer=CollectionSerializer(collection)
    return Response(serializer.data)