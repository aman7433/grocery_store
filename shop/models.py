from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(max_length=200,blank=True)

class Product(models.Model):
    name=models.CharField(max_length=30)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    stock=models.IntegerField()

class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

class Order(models.Model):
    status_choices=[
        ('pending','pending'),
        ('approved','approved'),
        ('delivered','delivered'),

    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(CartItem)
    total_price=models.DecimalField(decimal_places=2, max_digits=10)
    created_at=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=status_choices,default='pending')
