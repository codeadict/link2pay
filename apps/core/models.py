# -*- coding: utf-8 -*-#
import datetime
import random
import string
import hashlib
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from django.utils.http import urlquote_plus
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save


def get_hexdigest(algorithm, salt, raw_password):
    """Generate password hash."""
    return hashlib.new(algorithm, smart_str(salt + raw_password)).hexdigest()


def create_password(algorithm, raw_password):
    """Create salted, hashed password."""
    salt = os.urandom(5).encode('hex')
    hsh = get_hexdigest(algorithm, salt, raw_password)
    return '$'.join((algorithm, salt, hsh))


class UserProfile(models.Model):
    """Each user gets a profile."""
    username = models.CharField(max_length=255, default='', unique=True)
    password = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True, null=True)
    image = models.ImageField(
        upload_to="profiles", default='', blank=True, null=True)
    confirmation_code = models.CharField(
        max_length=255, default='', blank=True)

    created_on = models.DateTimeField(
        auto_now_add=True, default=datetime.datetime.now)
    
    deleted = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(User, null=True, editable=False, blank=True)

    def __unicode__(self):
        if self.deleted:
            return ugettext('Anonymous')
        return self.email or self.username
    
    def generate_confirmation_code(self):
        if not self.confirmation_code:
            self.confirmation_code = ''.join(random.sample(string.letters +
                                                           string.digits, 60))
        return self.confirmation_code
    
    def set_password(self, raw_password, algorithm='sha512'):
        """
        Set User Password
        """
        self.password = create_password(algorithm, raw_password)

    def check_password(self, raw_password):
        if '$' not in self.password:
            valid = (get_hexdigest('md5', '', raw_password) == self.password)
            if valid:
                # Upgrade an old password.
                self.set_password(raw_password)
                self.save()
            return valid

        algo, salt, hsh = self.password.split('$')
        return hsh == get_hexdigest(algo, salt, raw_password)
    
    
def create_profile(user, username=None):
    """Make a UserProfile for this django.contrib.auth.models.User."""
    if UserProfile.objects.all().count() == 0:
        user.is_superuser = True
        user.is_staff = True
    user.save()
    profile = UserProfile(id=user.id)
    profile.user = user
    profile.user_id = user.id
    if username:
        profile.username = username
    else:
        profile.username = user.username
    profile.email = user.email
    profile.save()
    return profile


## SIGNALS ##

def post_save_userprofile(sender, **kwargs):
    instance = kwargs.get('instance', None)
    created = kwargs.get('created', False)
    is_profile = isinstance(instance, UserProfile)


post_save.connect(post_save_userprofile, sender=UserProfile,
    dispatch_uid='users_post_save_userprofile')