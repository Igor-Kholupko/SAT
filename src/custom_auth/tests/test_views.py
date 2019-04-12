from django.test import TestCase, Client

from custom_auth.models import User


class RedirectFromStartPageTest(TestCase):
    def setUp(self):
        super(RedirectFromStartPageTest, self).setUp()
        authorized_user = User.objects.create(username='User')
        authorized_user.set_password('user_password')
        authorized_user.save()

        self.authorized_client = Client()
        self.login = self.authorized_client.login(username='User',
                                                      password='user_password')
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
