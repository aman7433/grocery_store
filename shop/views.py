from django.shortcuts import render
from .models import Category , CartItem, Product, Order
# Create your views here.

def category_list(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request, 'shop/category_list.html',context)

def product_list(request,category_id=None):
    if category_id:
        products=Product.objects.filter(category_id=category_id)
    else:
        products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'shop/product_list.html',context)
