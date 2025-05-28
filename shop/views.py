from django.shortcuts import get_object_or_404, render,redirect
from .models import Category , CartItem, Product, Order
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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

@login_required
def add_to_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart_item, created=CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity':1}
    )
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    messages.success(request,"Product added to cart")
    return redirect(view_cart)

@login_required
def view_cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    total=sum(item.product.price*item.quantity for item in cart_items)
    context={
        'cart_items':cart_items,
        'total':total
    }
    return render(request, 'shop/cart.html',context)

@login_required
def update_cart(request,item_id):
    if request.method=='POST':
        cart_item=get_object_or_404(CartItem,id=item_id,user=request.user)
        quantity=int(request.POST.get('quantity',1))

        if quantity>0:
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('view_cart')

@login_required
def remove_from_cart(request,item_id):
    cart_item=get_object_or_404(CartItem,id=item_id,user=request.user)
    cart_item.delete()
    messages.info(request,'Item is removed successfully')
    return redirect('view_cart')

@login_required
@transaction.atomic
def place_order(request):
    cart_items=CartItem.objects.select_related('product').filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request,'your cart is empty')
        return redirect(product_list)
    total=sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        total_price=Decimal(total)
    )
    order.items.set(cart_items)

    # Decrease product stock
    for item in cart_items:
        item.product.stock -= item.quantity
        item.product.save()

    # Clear the cart
    cart_items.delete()

    messages.success(request, "Order placed successfully!")
    return redirect('order_list')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})


def sign_up(request):
    if request.method=="POST":
        forms=UserCreationForm(request.POST)
        if forms.is_valid():
            user= forms.save()
            login(request,user)
            return redirect('category_list')
    else:
        forms=UserCreationForm()
    return render(request, 'shop/sign_up.html',{'form':forms})