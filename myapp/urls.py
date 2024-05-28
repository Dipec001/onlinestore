from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('products/item/', views.item_view, name='item-view'),
    path('cart/', views.cart_view, name='cart-view'),
    path('about/', views.about, name='about'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/',views.admin_view, name='admin'),
]