from .models import Cart, CartItem
from .views import get_cart
from django.utils.translation import get_language, gettext_lazy as _

def cart_item_count(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    cart_item_count = len(cart_items)

    context = {
        'header_placeholder': _('Search a drug name, a use case...'),
        'footer_email_placeholder': _('Email Address'),
        'cart_item_count': cart_item_count,
    }
    
    return context


def country_list(request):
    countries = [
        {'code': 'US', 'name': _('United States'), 'flag': 'images/flags/united-states.png', 'lang': 'en-us', 'currency_code': 'USD', 'currency_symbol': '$'},
        {'code': 'CA', 'name': _('Canada'), 'flag': 'images/flags/canada.png', 'lang': 'en-ca', 'currency_code': 'CAD', 'currency_symbol': '$'},
        {'code': 'GB', 'name': _('United Kingdom'), 'flag': 'images/flags/united-kingdom.png', 'lang': 'en-uk', 'currency_code': 'GBP', 'currency_symbol': '£'},
        {'code': 'AU', 'name': _('Australia'), 'flag': 'images/flags/australia.png', 'lang': 'en-au', 'currency_code': 'AUD', 'currency_symbol': '$'},
        {'code': 'DE', 'name': _('Germany'), 'flag': 'images/flags/germany.png', 'lang': 'de', 'currency_code': 'EUR', 'currency_symbol': '€'},
        {'code': 'FR', 'name': _('France'), 'flag': 'images/flags/france.png', 'lang': 'fr', 'currency_code': 'EUR', 'currency_symbol': '€'},
        {'code': 'RU', 'name': _('Russia'), 'flag': 'images/flags/russia.png', 'lang': 'ru', 'currency_code': 'RUB', 'currency_symbol': '₽'},
        {'code': 'SWE', 'name': _('Sweden'), 'flag': 'images/flags/sweden.png', 'lang': 'sv', 'currency_code': 'SEK', 'currency_symbol': 'kr'},
        {'code': 'ES', 'name': _('Spain'), 'flag': 'images/flags/spain.png', 'lang': 'es', 'currency_code': 'EUR', 'currency_symbol': '€'},
        {'code': 'IT', 'name': _('Italy'), 'flag': 'images/flags/italy.png', 'lang': 'it', 'currency_code': 'EUR', 'currency_symbol': '€'},
        {'code': 'CN', 'name': _('China'), 'flag': 'images/flags/china.png', 'lang': 'zh-hans', 'currency_code': 'CNY', 'currency_symbol': '¥'},
        {'code': 'SG', 'name': _('Singapore'), 'flag': 'images/flags/singapore.png', 'lang': 'en-sg', 'currency_code': 'SGD', 'currency_symbol': '$'},
        {'code': 'PT', 'name': _('Portugal'), 'flag': 'images/flags/portugal.png', 'lang': 'pt', 'currency_code': 'EUR', 'currency_symbol': '€'},
        {'code': 'CH', 'name': _('Switzerland'), 'flag': 'images/flags/switzerland.png', 'lang': 'de-ch', 'currency_code': 'CHF', 'currency_symbol': 'CHF'},  # Use 'de-CH' for Swiss German
        {'code': 'BE', 'name': _('Belgium'), 'flag': 'images/flags/belgium.png', 'lang': 'nl-be', 'currency_code': 'EUR', 'currency_symbol': '€'},  # Use 'nl-BE' for Flemish
        {'code': 'AE', 'name': _('UAE'), 'flag': 'images/flags/united-arab-emirates.png', 'lang': 'ar', 'currency_code': 'AED', 'currency_symbol': 'د.إ'},
        {'code': 'NL', 'name': _('Netherlands'), 'flag': 'images/flags/netherlands.png', 'lang': 'nl', 'currency_code': 'EUR', 'currency_symbol': '€'},
        {'code': 'JP', 'name': _('Japan'), 'flag': 'images/flags/japan.png', 'lang': 'ja', 'currency_code': 'JPY', 'currency_symbol': '¥'},
    ]

    current_language = get_language()
    current_country = next((c for c in countries if c['lang'] == current_language), countries[0])

    request.session['currency_code'] = current_country['currency_code']
    request.session['currency_symbol'] = current_country['currency_symbol']

    context = {
        'countries': countries,
        'current_country': current_country,
    }

    return context
