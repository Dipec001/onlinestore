from .models import Cart, CartItem
from .views import get_cart
import pycountry
from django.utils.translation import get_language

def cart_item_count(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_item_count = len(cart_items)
    
    return {'cart_item_count': cart_item_count}


def country_list(request):
    countries = [
        {'code': 'US', 'name': 'United States', 'flag': 'images/flags/united-states.png', 'lang': 'en'},
        {'code': 'CA', 'name': 'Canada', 'flag': 'images/flags/canada.png', 'lang': 'en'},
        {'code': 'GB', 'name': 'United Kingdom', 'flag': 'images/flags/united-kingdom.png', 'lang': 'en'},
        {'code': 'AU', 'name': 'Australia', 'flag': 'images/flags/australia.png', 'lang': 'en'},
        {'code': 'DE', 'name': 'Germany', 'flag': 'images/flags/germany.png', 'lang': 'de'},
        {'code': 'FR', 'name': 'France', 'flag': 'images/flags/france.png', 'lang': 'fr'},
        {'code': 'RU', 'name': 'Russia', 'flag': 'images/flags/russia.png', 'lang': 'ru'},
        {'code': 'SWE', 'name': 'Sweden', 'flag': 'images/flags/sweden.png', 'lang': 'sv'},
        {'code': 'ES', 'name': 'Spain', 'flag': 'images/flags/spain.png', 'lang': 'es'},
    ]

    current_language = get_language()
    current_country = next((c for c in countries if c['lang'] == current_language), countries[0])
    print(current_country)
    print(current_language)

    context = {
        'countries': countries,
        'current_country': current_country,
    }

    return context



