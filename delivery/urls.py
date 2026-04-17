from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.index),
    path('SignIn/', views.SignIn, name='SignIn'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('signup/', views.signup, name = 'signup'),
    path('signin/', views.signin, name = 'signin'),
    path('customer_home/', views.customer_home, name='customer_home'),
    path('signin/open_restaurant_page/', views.open_restaurant_page, name ='open_restaurant_page'),  
    path('signin/open_show_restaurant', views.open_show_restaurant ,name ='open_show_restaurant'),
    path('add_restaurant/', views.add_restaurant,name ='add_restaurant'),
    path('add_restaurant/open_update_restaurant/<int:restaurant_id>', views.open_update_restaurant,name ='open_update_restaurant'),
    path('update_restaurant/<int:restaurant_id>', views.update_restaurant, name="update_restaurant"),
    path('delete_restaurant/<int:restaurant_id>',views.delete_restaurant,name="delete_restaurant") ,  
    path('open_update_menu/<int:restaurant_id>', views.open_update_menu, name='open_update_menu'), 
    path('update_menu/<int:restaurant_id>',views.update_menu,name='update_menu'),
    path('view_menu/<int:restaurant_id>', views.view_menu, name='view_menu'),
    path('add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:cart_item_id>', views.update_cart_quantity, name='update_cart_quantity'),
]
