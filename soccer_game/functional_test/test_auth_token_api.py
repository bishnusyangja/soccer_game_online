from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from users.models import User


class AuthTokenAPITestCase(TestCase):
    client = APIClient()
    headers = {}
    username = ''
    password = ''
    url = "/api/auth-token/"

    def setUp(self):
        self.username = 'bishnu.bhattarai@gmail.com'
        self.password = '1'
        user = mommy.make(User, email=self.username, is_staff=True, is_superuser=True)
        user.set_password(self.password)
        user.save()

    def test_api_auth_token_with_no_data(self):
        resp = self.client.post(self.url, data={})
        self.assertEqual(resp.status_code, 400)

    def test_api_auth_token_with_invalid_data(self):
        resp = self.client.post(self.url, data={'username': self.username, 'password': 'abc'})
        self.assertEqual(resp.status_code, 400)

    def test_api_auth_token_with_valid_data(self):
        resp = self.client.post(self.url, data={'username': self.username, 'password': self.password})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.json().keys())
