# -*- coding: utf-8 -*-#
from django.contrib import admin
from django.db.models import get_model

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    """
    Products admin interface
    """
    list_display = ('upc', 'name', 'owner', 'price', 'date_added')
    list_filter = ('date_added', 'owner__username',)
    readonly_fields = ('get_qr_img',)
    
    
admin.site.register(Product, ProductAdmin)
    

