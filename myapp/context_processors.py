from .models import Cart, CartItem
from .views import get_cart

def cart_item_count(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_item_count = len(cart_items)
    
    return {'cart_item_count': cart_item_count}
