from django.urls import path
from .views import category_list,product_list

urlpatterns=[
    path('',category_list,name='clist'),
    path('product/',product_list,name='plist'),
]