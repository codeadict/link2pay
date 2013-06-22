# -*- coding: utf-8 -*-#
from django.contrib.auth.models import User
from django.db import IntegrityError

from core.models import UserProfile, create_profile


class L2PUserBackend(object):
    supports_anonymous_user = False
    supports_object_permissions = False

    def authenticate(self, username=None, password=None):
        try:
            if '@' in username:
                profile = UserProfile.objects.get(email=username)
            else:
                profile = UserProfile.objects.get(username=username)
            if profile.check_password(password):
                return profile.user
        except UserProfile.DoesNotExist:
            log.debug("Profile does not exist: %s" % (username,))
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None