from django.contrib import admin
from .models import Category,CartItem,Product,Order
# Register your models here.
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(CartItem)