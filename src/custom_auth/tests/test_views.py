from django.test import TestCase, Client

from custom_auth.models import User
from custom_auth.views import _teacher_url_parser


class RedirectFromStartPageTest(TestCase):
    def setUp(self):
        super(RedirectFromStartPageTest, self).setUp()
        authorized_user = User.objects.create(username='User')
        authorized_user.set_password('user_password')
        authorized_user.save()

        self.authorized_client = Client()
        self.login = self.authorized_client.login(username='User', password='user_password')
        self.anonymous_client = Client()

    def test_authorized_user_redirect(self):
        if self.login:
            response = self.authorized_client.get('')
            self.assertRedirects(response, '/dashboard/')

    def test_unauthorized_user_redirect(self):
        if self.login:
            self.authorized_client.logout()
            response = self.authorized_client.get('')
            self.assertRedirects(response, '/login/')

    def test_anonymous_user_redirect(self):
        response = self.anonymous_client.get('')
        self.assertRedirects(response, '/login/')


class AnotherPersonPageTest(TestCase):
    def setUp(self):
        super(AnotherPersonPageTest, self).setUp()
        authorized_user = User.objects.create(username='User')
        authorized_user.set_password('user_password')
        authorized_user.save()

        self.authorized_client = Client()
        self.login = self.authorized_client.login(username='User', password='user_password')
        self.anonymous_client = Client()

        password = User.objects.make_random_password()
        self.student_user = User.objects.create(username='6505004',
                                                password=password,
                                                first_name='Петр',
                                                surname='Петров',
                                                patronymic='Петрович')

        self.teacher = User.objects.create(username='IvanovII',
                                           password=password,
                                           first_name='Иван',
                                           surname='Иванов',
                                           patronymic='Иванович')

    def test_correct_student_page_request_by_authorized_user(self):
        if self.login:
            response = self.authorized_client.get('/personal-page/6505004/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['person'], self.student_user)

    def test_incorrect_student_page_request_by_authorized_user(self):
        if self.login:
            response = self.authorized_client.get('/personal-page/6505003/')
            self.assertEqual(response.status_code, 302)

    def test_correct_student_page_request_by_anonymous_user(self):
        response = self.anonymous_client.get('/personal-page/6505004/')
        self.assertRedirects(response, '/login/?next=/personal-page/6505004/')

    def test_incorrect_student_page_request_by_anonymous_user(self):
        response = self.anonymous_client.get('/personal-page/6505003/')
        self.assertRedirects(response, '/login/?next=/personal-page/6505003/')

    def test_simple_teacher_url(self):
        self.assertEqual('IvanovII', _teacher_url_parser('ivanov-i-i'))

    def test_complex_teacher_url(self):
        self.assertEqual('Ivanov-PetrovII', _teacher_url_parser('ivanov-petrov-i-i'))

    def test_correct_teacher_page_request_by_authorized_user(self):
        if self.login:
            response = self.authorized_client.get('/personal-page/ivanov-i-i/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['person'], self.teacher)

    def test_incorrect_teacher_page_request_by_authorized_user(self):
        if self.login:
            response = self.authorized_client.get('/personal-page/petrov-i-i/')
            self.assertEqual(response.status_code, 302)

    def test_correct_teacher_page_request_by_anonymous_user(self):
        response = self.anonymous_client.get('/personal-page/ivanov-i-i/')
        self.assertRedirects(response, '/login/?next=/personal-page/ivanov-i-i/')

    def test_incorrect_teacher_page_request_by_anonymous_user(self):
        response = self.anonymous_client.get('/personal-page/petrov-i-i/')
        self.assertRedirects(response, '/login/?next=/personal-page/petrov-i-i/')



