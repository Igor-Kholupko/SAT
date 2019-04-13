from custom_auth.management import SetUserTypeBaseCommand
from custom_auth.models import Group, Teacher, TEACHERS_GROUP


class Command(SetUserTypeBaseCommand):
    help = "Add specified user to teachers group."

    def handle_user(self, user):
        Teacher._default_manager.create(user=user, auditorium='000-0')
        group = Group._default_manager.get_or_create(name=TEACHERS_GROUP)[0]
        user.groups.add(group)
