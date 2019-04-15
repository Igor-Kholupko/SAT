from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from custom_auth.management import update_groups_permissions


class CustomAuthConfig(AppConfig):
    name = 'custom_auth'
    verbose_name = _("Custom authorization")

    def ready(self):
        post_migrate.connect(update_groups_permissions, sender=self, dispatch_uid='update_groups_permissions')
