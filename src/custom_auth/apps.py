from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CustomAuthConfig(AppConfig):
    name = 'custom_auth'
    verbose_name = _("Custom authorization")
