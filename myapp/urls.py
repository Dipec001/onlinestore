from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('products/<str:id>/', views.item_view, name='item-view'),
    path('cart/', views.cart_view, name='cart-view'),
    path('about/', views.about, name='about'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:drug_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:drug_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('subtract-from-cart/<int:drug_id>/', views.subtract_from_cart, name='subtract_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
]