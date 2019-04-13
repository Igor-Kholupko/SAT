import re

from django.test import TestCase

from custom_auth.models import Group, User, Student, Teacher
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
        self.teacher = Teacher.objects.create(user=self.teacher_user,
                                              auditorium='509a-5')
        self.student = Student.objects.create(user=self.student_user,
                                              group=self.student_group,
                                              faculty=0,
                                              year_of_studying=2,
                                              speciality=2)

    def test_get_faculty_abbreviation(self):
        faculty_full_name = self.student.get_faculty_display()
        faculty_abbreviation = ''.join(word[0] for word in re.split(r'\W+', faculty_full_name))
        self.assertEqual(faculty_abbreviation, self.student.get_faculty_abbreviation())

    def test_promotion_rates(self):
        next_year_of_study = self.student.year_of_studying + 1
        self.student.promotion_rates()
        self.assertEqual(next_year_of_study, self.student.year_of_studying)

    def test_simple_get_url(self):
        self.assertEqual('petrov-p-p', self.teacher.get_url())

    def test_complex_get_url(self):
        teacher_password = User.objects.make_random_password()
        teacher_user = User.objects.create(username='Tashlukova-BushkevichII',
                                           password=teacher_password,
                                           first_name='Ия',
                                           surname='Ташлыкова-Бушкевич',
                                           patronymic='Игоревна')

        teacher = Teacher.objects.create(user=teacher_user,
                                         auditorium='409a-4')
        self.assertEqual('tashlukova-bushkevich-i-i', teacher.get_url())


class GroupTest(TestCase):
    def setUp(self):
        self.group = Group.objects.get(pk=1)

    def test_model_creation(self):
        with self.assertRaises(PermissionError):
            new_group = Group(name='student')
            new_group.save()
        with self.assertRaises(PermissionError):
            Group.objects.create(name='student')

    def test_model_deleting(self):
        with self.assertRaises(PermissionError):
            self.group.delete()

