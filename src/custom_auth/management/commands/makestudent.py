from custom_auth.management import SetUserTypeBaseCommand
from custom_auth.models import Group, Student, STUDENTS_GROUP, StudyGroup


class Command(SetUserTypeBaseCommand):
    help = "Add specified user to teachers group."

    def handle_user(self, user):
        Student._default_manager.create(
            user=user, group=StudyGroup.objects.get_or_create(number=000000)[0],
            faculty=0, year_of_studying=0, speciality=0
        )
        group = Group._default_manager.get_or_create(name=STUDENTS_GROUP)[0]
        user.groups.add(group)
