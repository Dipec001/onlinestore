from .models import Cart, CartItem
from .views import get_cart
from django.utils.translation import get_language, gettext_lazy as _

def cart_item_count(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_item_count = len(cart_items)
    
    return {'cart_item_count': cart_item_count}


def country_list(request):
    countries = [
        {'code': 'US', 'name': _('United States'), 'flag': 'images/flags/united-states.png', 'lang': 'en-us', 'currency_code': 'USD'},
        {'code': 'CA', 'name': _('Canada'), 'flag': 'images/flags/canada.png', 'lang': 'en-ca', 'currency_code': 'CAD'},
        {'code': 'GB', 'name': _('United Kingdom'), 'flag': 'images/flags/united-kingdom.png', 'lang': 'en-uk', 'currency_code': 'GBP'},
        {'code': 'AU', 'name': _('Australia'), 'flag': 'images/flags/australia.png', 'lang': 'en-au', 'currency_code': 'AUD'},
        {'code': 'DE', 'name': _('Germany'), 'flag': 'images/flags/germany.png', 'lang': 'de', 'currency_code': 'EUR'},
        {'code': 'FR', 'name': _('France'), 'flag': 'images/flags/france.png', 'lang': 'fr', 'currency_code': 'EUR'},
        {'code': 'RU', 'name': _('Russia'), 'flag': 'images/flags/russia.png', 'lang': 'ru', 'currency_code': 'RUB'},
        {'code': 'SWE', 'name': _('Sweden'), 'flag': 'images/flags/sweden.png', 'lang': 'sv', 'currency_code': 'SEK'},
        {'code': 'ES', 'name': _('Spain'), 'flag': 'images/flags/spain.png', 'lang': 'es', 'currency_code': 'EUR'},
        {'code': 'IT', 'name': _('Italy'), 'flag': 'images/flags/italy.png', 'lang': 'it', 'currency_code': 'EUR'},
        {'code': 'CN', 'name': _('China'), 'flag': 'images/flags/china.png', 'lang': 'ch', 'currency_code': 'CNY'},
        {'code': 'SG', 'name': _('Singapore'), 'flag': 'images/flags/singapore.png', 'lang': 'en-sg', 'currency_code': 'SGD'},
        {'code': 'PT', 'name': _('Portugal'), 'flag': 'images/flags/portugal.png', 'lang': 'pr', 'currency_code': 'EUR'},
        {'code': 'CH', 'name': _('Switzerland'), 'flag': 'images/flags/switzerland.png', 'lang': 'swi', 'currency_code': 'CHF'},
        {'code': 'BE', 'name': _('Belgium'), 'flag': 'images/flags/belgium.png', 'lang': 'be', 'currency_code': 'EUR'},
        {'code': 'AE', 'name': _('UAE'), 'flag': 'images/flags/united-arab-emirates.png', 'lang': 'ar', 'currency_code': 'AED'},
        {'code': 'NL', 'name': _('Netherlands'), 'flag': 'images/flags/netherlands.png', 'lang': 'nl', 'currency_code': 'EUR'},
    ]

    current_language = get_language()
    current_country = next((c for c in countries if c['lang'] == current_language), countries[0])

    # Check if 'currency_code' is already in session
    if 'currency_code' not in request.session:
        # Set default currency code based on current language
        request.session['currency_code'] = current_country['currency_code']

    context = {
        'countries': countries,
        'current_country': current_country,
    }

    return context