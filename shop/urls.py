from django.urls import path
# from .views import category_list,product_list,view_cart,add_to_cart,update_cart,remove_from_cart,place_order,order_list,order_detail
from . import views

urlpatterns=[
    path('', views.category_list, name='category_list'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:category_id>/', views.product_list, name='product_list_by_category'),

    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('order/place/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),


    path('accounts/signup/', views.sign_up, name='signup'),


    
]