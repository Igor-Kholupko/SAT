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
