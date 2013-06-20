# -*- coding: utf-8 -*-
from django import template
from django.conf import settings


register = template.Library()

def priceformat(price):
    FORMAT = getattr(settings, 'SHOP_PRICE_FORMAT', '%0.2f')
    if not price and price != 0:
        return ''
    return FORMAT % price
register.filter(priceformat)