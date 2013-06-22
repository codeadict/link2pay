# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.html import format_html
from django.forms import BaseForm


register = template.Library()

def priceformat(price):
    FORMAT = getattr(settings, 'SHOP_PRICE_FORMAT', '%0.2f')
    if not price and price != 0:
        return ''
    return FORMAT % price
register.filter(priceformat)

@register.inclusion_tag('includes/form.html', takes_context=True)
def render_form(context, form_obj):
    if not isinstance(form_obj, BaseForm):
        raise TypeError("Error including form, it's not a form, it's a %s" % type(form_obj))
    context.update({'form': form_obj})
    return context