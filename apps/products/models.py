# -*- coding: utf-8 -*-
import string
import random
import re
from urllib import quote
from urllib2 import urlopen, Request, HTTPError
try:
    import json
except ImportError:
    import simplejson as json

from cStringIO import StringIO
from decimal import Decimal

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site

from core.util import CurrencyField, slugify
from core.PyQRNative import *


def upc_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class Product(models.Model):
    """
    Base product model
    """
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    upc = models.CharField(_("Product Code"), max_length=64, blank=True, null=True,
                           unique=True,
        help_text=_("Universal Product Code (UPC) is an identifier for "
                    "a product which is not specific to a particular "
                    " supplier. Eg an ISBN for a book."))
    slug = models.SlugField(verbose_name=_('Slug'), unique=True)
    image = models.ImageField(upload_to="product_images", max_length=1024 * 200,
                             blank=False, null=False, verbose_name=_("Product Image"))
    qr_code = models.ImageField(
        upload_to="qr_codes/url/", null=True, blank=True,
        editable=False,
        verbose_name=_('QR Code')
    )
    owner = models.ForeignKey(User, null=False, blank=False, verbose_name=_('User'))
    active = models.BooleanField(default=False, verbose_name=_('Active'))
    date_added = models.DateTimeField(auto_now_add=True,
        verbose_name=_('Date added'))
    price = CurrencyField(verbose_name=_('Unit price')) 
    
    class Meta(object):
        app_label = 'products'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', (), {'slug':self.upc})
    
    @property
    def get_short_url(self, all_response=False):
        """
        Gets a short URL for sharing using goo.gl service
        """
        request = None
        url = ''.join(['http://', get_current_site(request).domain, self.get_absolute_url()])
        if not re.match('http://', url):
            raise Exception(_('Invalid URL'))
        
        header = { "Content-Type": "application/json" }
        params = { "longUrl": url }
        gurl = 'https://www.googleapis.com/urlshortener/v1/url'
        
        req = urlopen(Request(gurl, json.dumps(params), header))
        json_data = req.read()

        if not all_response:
            data = json.loads(json_data)
            if 'id' in data:
                return json.loads(json_data)['id']
            return u""
        return json_data
    
    
    def get_price(self):
        """
        Return the price for this item
        """
        return self.unit_price
    
    def get_qr_img(self):
        """
        Gets generated QR image url
        to show on admin or product details easier
        """
        return '<img src="%s" width="200" alt="QR CODE"/>' % (self.qr_code.url)
    get_qr_img.allow_tags = True
    
    @property
    def can_be_purchased(self):
        return self.active
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically add UPC and unique slug
        """
        if not self.upc:
            self.upc = upc_generator()
        
        count = 1
        if not self.slug:
            slug = slugify(self.name)
            self.slug = slug
            while True:
                existing = Product.objects.filter(slug=self.slug)
                if len(existing) == 0:
                    break
                self.slug = "%s-%s" % (slug, count + 1)
                count += 1
        return super(Product, self).save(*args, **kwargs)
    
def urlqrcode_pre_save(sender, instance, **kwargs):    
    if not instance.pk:
        instance._QRCODE = True
    else:
        if hasattr(instance, '_QRCODE'):
            instance._QRCODE = False
        else:
            instance._QRCODE = True
                
def urlqrcode_post_save(sender, instance, **kwargs):
    if instance._QRCODE:
        instance._QRCODE = False
        if instance.qr_code:
            instance.qr_code.delete()
        qr = QRCode(20, QRErrorCorrectLevel.L)
        
        qr.addData(instance.upc)
        qr.make()
        image = qr.makeImage()
     
        #Save image to string buffer
        image_buffer = StringIO()
        image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
     
        #Here we use django file storage system to save the image.
        file_name = 'product_%s_%s.jpg' % (instance.owner.username, instance.name)
        file_object = File(image_buffer, file_name)
        content_file = ContentFile(file_object.read())
        instance.qr_code.save(file_name, content_file, save=True)
 
#Signals
models.signals.pre_save.connect(urlqrcode_pre_save, sender=Product)
models.signals.post_save.connect(urlqrcode_post_save, sender=Product)

    
