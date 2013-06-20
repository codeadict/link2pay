# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _


class PaypalPayment(object):
    """
    Backend to accept paypal payments
    """
    name = "Paypal"
    url_namespace = "paypal"
    