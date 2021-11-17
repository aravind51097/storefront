
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Collection, Product, Reviews
from .serializer import CollectionSerializer, ProductSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
   
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


    def destroy(self, request, *args, **kwargs):
        product=get_object_or_404(Product,pk=kwargs['pk'])
        if product.orderitem_set.count()>0:
            return Response(
                {"error":'item cant be deleted cuz its ordered'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    


class CollectionViewSet(ModelViewSet):

    queryset=Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class=CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection,pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    queryset=Reviews.objects.all()
    serializer_class=ReviewSerializer

    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}