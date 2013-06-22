from django.forms import ModelForm
from products.models import Product


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'active', 'price']
