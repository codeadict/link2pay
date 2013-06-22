from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from products.views import MyProducts, ProductDetails

from core.views import ContactView

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    url(r'^myproducts$', MyProducts.as_view(), name='product_list'),
    url(r'^contact/$',
        ContactView.as_view(template_name='contact.html'),
        name='contact'),
    url(r'^(?P<slug>[\w-]+)/*$', ProductDetails.as_view(), name="product_detail"),
    url(r'^$', include('products.urls')),
    
    # url(r'^link2pay/', include('link2pay.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^manager/', include(admin.site.urls)),
    
)

#Add Flatpages for static pages
# urlpatterns += patterns('django.contrib.flatpages.views',
#     (r'^(?P<url>.*)$', 'flatpage'),
# )
