# -*- coding: utf-8 -*-#
from __future__ import with_statement
import urllib2

from django.http import HttpResponseRedirect, Http404
from django.views.generic import FormView

from core.forms import ContactForm, AuthenticationForm


def login(request):
    """Log the user in."""

    request = _process_redirect(request)

    if request.user.is_authenticated():
        user = request.user.get_profile()
        redirect_url = _get_redirect_url(request)
        olang = get_language()
        return _after_login_redirect(redirect_url, user)

    logout(request)

    dashboard_url = reverse('product_add')
    redirect_field_value = request.session.get(
        REDIRECT_FIELD_NAME, dashboard_url) or dashboard_url
    try:
        redirect_field_value = urllib2.quote(redirect_field_value)
    except KeyError:
        # Unicode Issue
        pass
    extra_context = {
        'redirect_field_name': REDIRECT_FIELD_NAME,
        'redirect_field_value': redirect_field_value,
    }

    r = auth_views.login(request, template_name='users/login.html',
                         authentication_form=AuthenticationForm,
                         extra_context=extra_context)

    if isinstance(r, http.HttpResponseRedirect):
        user = request.user.get_profile()

        if request.POST.get('remember_me', None):
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)

        redirect_url = _get_redirect_url(request)
        if redirect_url:
            redirect_url = force_language_in_url(
                redirect_url, olang, user.preflang)
            return _after_login_redirect(redirect_url, user)

    elif request.method == 'POST':
        messages.error(request, _('Incorrect username, email or password.'))
        # run through auth_views.login again to render template with messages.
        r = auth_views.login(request, template_name='users/login.html',
                         authentication_form=AuthenticationForm)
    return r

class ContactView(FormView):
    form_class = ContactForm
    
    def get_initial(self):
        initial = super(ContactView, self).get_initial()       
        return initial
    
    def form_valid(self, form):
        target_url = form.save()
        return HttpResponseRedirect(target_url)