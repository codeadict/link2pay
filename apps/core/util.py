# -*- coding: utf-8 -*-

import re
import unicodedata
from decimal import Decimal

from django import forms
from django.core import urlresolvers
from django.core.validators import ValidationError, validate_slug
from django.utils.encoding import smart_unicode
from django.conf import settings
from django.db.models.fields import DecimalField
from django.utils.translation import ugettext_lazy as _

# Extra characters outside of alphanumerics that we'll allow on slugs.
SLUG_OK = '-_'


def slugify(s, ok=SLUG_OK, lower=True):
    # L and N signify letter/number.
    # http://www.unicode.org/reports/tr44/tr44-4.html#GC_Values_Table
    rv = []
    for c in smart_unicode(s):
        cat = unicodedata.category(c)[0]
        if cat in 'LN' or c in ok:
            rv.append(c)
        if cat == 'Z': # space
            rv.append(' ')
    new = re.sub('[-\s]+', '-', ''.join(rv).strip())
    return new.lower() if lower else new


def slug_validator(s, ok=SLUG_OK, lower=True):
    """
Raise an error if the string has any punctuation characters.

Regexes don't work here because they won't check alnums in the right
locale.
"""
    if not (s and slugify(s, ok, lower) == s):
        raise ValidationError(validate_slug.message,
                              code=validate_slug.code)

class CurrencyField(DecimalField):
    """
    A CurrencyField is simply a subclass of DecimalField with a fixed format:
    max_digits = 30, decimal_places=10, and defaults to 0.00
    """
    def __init__(self, **kwargs):
        defaults = {
            'max_digits': 30,
            'decimal_places': 2,
            'default': Decimal('0.0')
        }
        defaults.update(kwargs)
        super(CurrencyField, self).__init__(**defaults)

    def south_field_triple(self): # pragma: no cover
        """
        Returns a suitable description of this field for South.
        This is excluded from coverage reports since it is pretty much a piece
        of South itself, and does not influence program behavior at all in
        case we don't use South.
        """
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DecimalField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
    

class UsernameField(forms.Field):
    widget = forms.widgets.TextInput(attrs={'autocomplete': 'off'})

    def clean(self, value):
        super(UsernameField, self).clean(value)
        slug_validator(value, lower=False)
        try:
            func, args, kwargs = urlresolvers.resolve("/%s/" % (value,))
            if callable(func) and args == ():
                if 'username' not in kwargs.keys():
                    raise forms.ValidationError(
                        _('Please choose another username.'))
        except urlresolvers.Resolver404:
            pass
        if value in settings.INVALID_USERNAMES:
            raise forms.ValidationError(_('Please choose another username.'))
        return value