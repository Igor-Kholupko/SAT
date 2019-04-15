from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class SetUserTypeBaseCommand(BaseCommand):
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser):
        parser.add_argument(
            '%s' % self.UserModel.USERNAME_FIELD,
            help='Specifies the user to add to group.',
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Command available only in DEBUG.")
        user = self.UserModel._default_manager.filter(
            **{self.UserModel.USERNAME_FIELD: options[self.UserModel.USERNAME_FIELD]}
        )
        if not user.exists():
            raise CommandError("User with specified %s not found." % self.UserModel.USERNAME_FIELD)
        self.handle_user(user.first())

    def handle_user(self, user):
        raise NotImplementedError('subclasses of SetUserTypeBaseCommand must provide a handle_user() method')


def update_groups_permissions(*, apps=None, **kwargs):
    if apps is None:
        return
    try:
        Group = apps.get_model('custom_auth', 'Group')
    except LookupError:
        return

    OldGroup = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    from django.db.models import Q
    from functools import reduce
    from custom_auth.consts import GROUP_PERMISSIONS

    with transaction.atomic():
        for group, permissions in GROUP_PERMISSIONS.items():
            group = Group.objects.get_or_create(group_ptr=OldGroup.objects.get_or_create(name=group)[0], name=group)[0]
            group.permissions.clear()
            group.permissions.add(*Permission.objects.filter(
                reduce(Q.__or__, [Q(codename=permission['codename'], content_type__app_label=permission['app'].lower(),
                                    content_type__model=permission['model'].lower()) for permission in permissions])
            ))
