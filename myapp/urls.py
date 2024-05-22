from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('products/item/', views.item_view, name='item-view'),
    path('cart/', views.cart_view, name='cart-view'),

]