import requests
import os
from decimal import Decimal, getcontext

def convert_currency(amount, to_currency):
    if to_currency == 'USD':
        return amount

    api_key = os.getenv("API_KEY")
    url = f"https://api.exchangerate-api.com/v4/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        rates = response.json().get('rates', {})
        conversion_rate = rates.get(to_currency)

        if conversion_rate is None:
            return amount

        # Convert conversion_rate to Decimal
        conversion_rate = Decimal(conversion_rate)

        return amount * conversion_rate
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return amount
