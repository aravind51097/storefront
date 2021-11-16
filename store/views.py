from django.shortcuts import get_object_or_404
from rest_framework import serializers,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializer import ProductSerializer



@api_view()
def product_list(request):
    query_set=Product.objects.all()
    serializer=ProductSerializer(query_set,many=True)
    return Response(serializer.data)

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

@api_view()
def product_details(request,id):
    product=get_object_or_404(Product,pk=id)
    serializer=ProductSerializer(product)
    return Response(serializer.data)
