# -*- coding: utf-8 -*-#
from __future__ import with_statement

import re

from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext as _


def check_password_complexity(password):
    message = _('Password must be at least 8 characters long ')
    message += _('and contain both numbers and letters.')
    if len(password) < 8 or not (
        re.search('[A-Za-z]', password) and re.search('[0-9]', password)):
        return message
    return None


class AuthenticationForm(auth_forms.AuthenticationForm):
    """
    Login Form
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'tabindex': '1'}))
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'tabindex': '2'},
                                   render_value=False))
    remember_me = forms.BooleanField(required=False,
                                     widget=forms.CheckboxInput(
                                         attrs={'tabindex': '3'}))


class RegisterForm(forms.ModelForm):
    """
    User Registration Form
    """
    username = UsernameField()
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(render_value=False))
    recaptcha = captcha_fields.ReCaptchaField()
    email_confirm = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        if not settings.RECAPTCHA_PRIVATE_KEY:
            del self.fields['recaptcha']
            
    def clean_password(self):
        password = self.cleaned_data['password']
        message = check_password_complexity(password)
        if message:
            self._errors['password'] = forms.util.ErrorList([message])
        return password
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError(
                _('This Username already exists.'))
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email or not email.strip():
            raise forms.ValidationError(_('This field is required.'))
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('User with this Email already exists.'))
        return email
    
    def clean(self):
        super(RegisterForm, self).clean()
        data = self.cleaned_data
        if 'password' in data and 'password_confirm' in data:
            if data['password'] != data['password_confirm']:
                self._errors['password_confirm'] = forms.util.ErrorList([
                    _('Passwords do not match.')])
        if 'email' in data and 'email_confirm' in data:
            if data['email'] != data['email_confirm']:
                self._errors['email_confirm'] = forms.util.ErrorList([
                    _('Email addresses do not match.')])
        return data



class ContactForm(forms.Form):
    """
    Formulario de Contacto
    """
    name = forms.CharField(label='Nombre')
    company = forms.CharField(label='Empresa')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Teléfono')
    message = forms.CharField(label='Mensaje', widget=forms.Textarea)
    