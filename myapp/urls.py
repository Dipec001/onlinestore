from django.urls import path, include
from . import views
from django.views.i18n import set_language

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', views.contact, name='contact'),
    path('products/category/<int:category_id>/', views.products, name='products_by_category'),  # Pattern with category ID
    path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('faqs/', views.faqs, name='faqs'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>', views.blog_detail, name='blog-detail'),
    path('products/<str:id>/', views.item_view, name='item-view'),
    path('cart/', views.cart_view, name='cart-view'),
    path('about/', views.about, name='about'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:drug_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:drug_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('subtract-from-cart/<int:drug_id>/', views.subtract_from_cart, name='subtract_from_cart'),
    # path('checkout/', views.checkout_view, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
]