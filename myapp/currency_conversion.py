import requests
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings
import os

def fetch_exchange_rates(base_currency='USD'):
    cache_key = f"exchange_rates_{base_currency}"
    rates = cache.get(cache_key)

    if not rates:
        api_key = os.getenv('API_KEY')  # Replace with your actual API key
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            rates = response.json().get('rates', {})
            cache.set(cache_key, rates, timeout=60*60)  # Cache for 1 hour
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            rates = {}

    return rates

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount

    rates = fetch_exchange_rates(from_currency)
    conversion_rate = rates.get(to_currency)

    if conversion_rate is None:
        raise ValueError(f"Conversion rate for {to_currency} not found")

    # Convert conversion_rate to Decimal
    conversion_rate = Decimal(conversion_rate)
    return amount * conversion_rate
