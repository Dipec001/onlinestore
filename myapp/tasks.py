# tasks.py
from celery import shared_task
from .models import Drug
import requests
from decimal import Decimal

@shared_task
def update_currency_rates():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    rates = data['rates']

    for drug in Drug.objects.all():
        drug.price_en_us = drug.price * Decimal(rates.get('USD'))
        drug.price_zh_hans = drug.price * Decimal(rates['CNY'])
        drug.price_pt = drug.price * Decimal(rates.get('EUR'))
        drug.price_de = drug.price * Decimal(rates.get('EUR'))
        drug.price_de_CH = drug.price * Decimal(rates.get('CHF'))
        drug.price_en_uk = drug.price * Decimal(rates.get('GBP'))
        drug.price_en_ca = drug.price * Decimal(rates.get('CAD'))
        drug.price_en_au = drug.price * Decimal(rates.get('AUD'))
        drug.price_en_sg = drug.price * Decimal(rates.get('SGD'))
        drug.price_fr = drug.price * Decimal(rates.get('EUR'))
        drug.price_sv = drug.price * Decimal(rates.get('SEK'))
        drug.price_es = drug.price * Decimal(rates.get('EUR'))
        drug.price_nl = drug.price * Decimal(rates.get('EUR'))
        drug.price_nl_BE = drug.price * Decimal(rates.get('EUR'))
        drug.price_it = drug.price * Decimal(rates.get('EUR'))
        drug.price_ru = drug.price * Decimal(rates.get('RUB'))
        drug.price_ar = drug.price * Decimal(rates.get('AED'))
        drug.price_ja = drug.price * Decimal(rates.get('JPY'))
        drug.save()
