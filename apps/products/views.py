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
        
        def form_valid(self, form):
            try:
                if self.request.user.is_authenticated():
                    user = self.request.user.get_profile()
                form.owner = user
                form.save(commit = True)
                messages.success(self.request, _(u"Product %s created correctly.") % form.cleaned_data['name'])
            except:
                messages.error(self.request, _(u"There was an error creating this Product."))
            return super(ProductCreate, self).form_valid(form)
        
        
class MyProducts(ListView, TemplateResponseMixin):
    """
    Show products for specific user
    """
    context_object_name = "product_list"
    template_name = "my_products.html"
     
    def get_queryset(self):
        """Override get_querset so we can filter on request.user """
        return Product.objects.filter(owner=self.request.user)
    
class ProductDetails(DetailView):
    """
    Product Detail View
    """
    model = Product
    slug_field = "upc"
    context_object_name='product'
    template_name="pdetails.html"
    
        
        

