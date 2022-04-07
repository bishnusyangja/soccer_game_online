import json

from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from users.models import User


class UserAPITestCase(TestCase):
    client = APIClient()
    headers = {}
    url = '/users/api/'

    def setUp(self):
        username = 'bishnu.bhattarai@infynitee.com.au'
        password = 1
        user = mommy.make(User, email=username, is_staff=True)
        user.set_password(password)
        user.save()
        resp = self.client.post('/api/auth-token/', data={'username': username, 'password': password})
        self.auth_token = resp.json().get('token', '')
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.auth_token}', 'CONTENT_TYPE': 'application/json'}

    def test_user_list_api_with_no_headers(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_user_list_api_with_authorization_headers(self):
        resp = self.client.get(self.url, **self.headers)
        self.assertEqual(resp.status_code, 200)

    def test_user_list_api_response_content(self):
        cnt = 3
        mommy.make(User, cnt)
        resp = self.client.get(self.url, **self.headers)
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content['count'], cnt+1)
        self.assertIn('email', content[0].keys())
        self.assertIn('first_name', content[0].keys())
        self.assertIn('last_name', content[0].keys())
        self.assertIn('mobile', content[0].keys())
        self.assertIn('is_active', content[0].keys())
        self.assertIn('pk', content[0].keys())

    def test_user_registration_api_with_no_headers(self):
        data = {}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 401)

    def test_user_registration_api_with_headers_but_no_data(self):
        data = {}
        resp = self.client.post(self.url, data=data, **self.headers)
        self.assertEqual(resp.status_code, 400)

    def test_user_registration_api_with_headers_and_data(self):
        data = {'email': 'sunyahealthnepal@gmail.com', 'first_name': 'Ramesh', 'last_name': 'Bhandari'}
        resp = self.client.post(self.url, data=data, **self.headers)
        self.assertEqual(resp.status_code, 200)

    def test_user_update_api_with_patch(self):
        user = mommy.make(User)
        data = {'is_active': True}
        resp = self.client.patch(f'{self.url}{user.pk}/', data=data, **self.headers)
        self.assertEqual(resp.status_code, 200)

    def test_user_update_api_with_put(self):
        user = mommy.make(User)
        data = {}
        resp = self.client.put(f'{self.url}{user.pk}/', data=json.dumps(data), **self.headers)
        self.assertEqual(resp.status_code, 400)

    def test_user_delete_api(self):
        # todo: is_deleted not implemented in user model
        user = mommy.make(User)
        resp = self.client.delete(f'{self.url}{user.pk}/', **self.headers)
        self.assertEqual(resp.status_code, 204)