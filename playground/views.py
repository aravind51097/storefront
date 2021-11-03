from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,F,Value,Func
from django.db.models.aggregates import Count,Min,Max,Sum,Avg 
from store.models import Collection, Customer, Order, Product,OrderItem




def say_hello(request):
    product=Product.objects.filter(unit_price__gt=10,unit_price__lt=20)
    
    return render(request, 'hello.html', {'name': 'filter','products':product,})


def complex_query(request):
    Q_set=Product.objects.filter(Q(inventory__lt=20) | Q(unit_price__lt=10) )
    return render(request,'complex_query.html',{'name':'complex_query','products':Q_set})

def sorting(request):
    Q_set=Product.objects.filter(Q(inventory__lt=20)).order_by('unit_price')
    latest=Product.objects.latest('unit_price')
    earliest=Product.objects.earliest('unit_price')
    return render(request,'sorting_data.html',{'name':'sorting data','products':Q_set})

def inner_join(request):
    Q_set=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
 
    return render(request,'inner.html',{'name':'inner_join-uisng_VALUES','products':Q_set})


def select_related(request):
    order=Order.objects.select_related('customer').order_by('-placed_at')[0:5]
 
    return render(request,'select_related.html',{'name':'select_realated','orders':order})
def aggregate(request):
    result=Product.objects.aggregate(count=Count('id'))
    result1=Product.objects.filter(collection__id=1).aggregate(Count=Count('id'))
    result2=Product.objects.aggregate(min_price=Min('unit_price'))

    return render(request,'aggregate.html',{'result':result,'result1':result1,'result2':result2})

def annotate(request):
    full_name=Customer.objects.annotate(full_name=Func(F('first_name'),Value(''),F('last_name'),function='CONCAT '))
    
    
    return render(request, 'annotate.html', {'full_name':full_name})

def inserting_data(request):
    #need to craeate a object 1st
    collection=Collection()
    # set the values to the firld
    collection.title='video game'
    collection.featured_product=Product(pk=1)
    collection.save()

    

    return render(request,'inserting_data.html',{'name':'aravind'})     