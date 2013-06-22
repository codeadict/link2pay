from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from products.views import ProductCreate

urlpatterns = patterns('',
    url(r'^$', ProductCreate.as_view(), name="product_add"),
)
