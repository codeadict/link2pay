# -*- coding: utf-8 -*-
from products.models import Product
from products import forms


from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin

from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404

from django.contrib import messages


class ProductCreate(FormView, TemplateResponseMixin):
        form_class = forms.ProductCreateForm
        template_name="add.html"
        success_url = '/'
        
        def dispatch(self, request, *args, **kwargs):   
            return super(ProductCreate, self).dispatch(request, *args, **kwargs)
        
        def get_context_data(self, **kwargs):
            kwargs['create_form'] = kwargs.pop('form', None)
            return super(ProductCreate, self).get_context_data(**kwargs)
