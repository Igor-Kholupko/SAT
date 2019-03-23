import re

from django.test import TestCase

from custom_auth.models import User, Student
from labs.models import Group as StudyGroup


class UserTest(TestCase):
    def setUp(self):
        student_password = User.objects.make_random_password()
        self.student_user = User.objects.create(username='6505001',
                                                password=student_password,
                                                first_name='Иван',
                                                surname='Иванов',
                                                patronymic='Иванович')

        teacher_password = User.objects.make_random_password()
        self.teacher_user = User.objects.create(username='PetrovPP',
                                                password=teacher_password,
                                                first_name='Петр',
                                                surname='Петров',
                                                patronymic='Петрович')

        self.student_group = StudyGroup.objects.create(number='650501')
        self.student = Student.objects.create(user=self.student_user,
                                              group=self.student_group,
                                              faculty=3,
                                              year_of_studying=2,
                                              specialty=2)

    def test_get_faculty_abbreviation(self):
        faculty_full_name = self.student.get_faculty_display()
        faculty_abbreviation = ''.join(word[0] for word in re.split(r'\W+', faculty_full_name))
        self.assertEqual(faculty_abbreviation, self.student.get_faculty_abbreviation())


class GroupTest(TestCase):
    pass
