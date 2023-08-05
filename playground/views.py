from django.shortcuts import render
from store.models import Customer, Product, Order, OrderItem
# Create your views here.

def say_hello(request):
    products = Product.objects.all().order_by('title')
    products_inventory = Product.objects.filter(inventory__lt=10)
    order_by_customer = OrderItem.objects.values('product__id').distinct()
    return render(request,'say_hello.html',{
            'orders':order_by_customer
            }
            )
