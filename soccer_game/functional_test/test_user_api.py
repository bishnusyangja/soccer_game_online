import json

from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from users.models import User


class UserRegisterAPITestCase(TestCase):
    # for patch and put request this APIClient needs content_type="application/json"
    client = APIClient()
    url = '/register/'

    def test_user_create_with_no_data(self):
        data = {}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_user_create_with_data(self):
        data = {'email': 'nepalisheaven@gmail.com', 'first_name': 'Ramesh', 'last_name': 'Bhandari'}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 201)

    def test_user_create_with_logged_in_user(self):
        username = 'bishnu.bhattarai@gmail.com'
        password = '1'
        user = mommy.make(User, email=username, is_staff=True)
        user.set_password(password)
        user.save()
        self.client.login(username=username, password=password)
        data = {'email': 'nepalisheaven@gmail.com', 'first_name': 'Ramesh', 'last_name': 'Bhandari'}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 403)


class UserAPITestCase(TestCase):
    # for patch and put request this APIClient needs content_type="application/json"
    client = APIClient()
    url = "/user/"

    def setUp(self):
        username = 'bishnu.bhattarai@gmail.com'
        password = '1'
        user = mommy.make(User, email=username, is_staff=True)
        user.set_password(password)
        user.save()
        self.client.login(username=username, password=password)

    def test_user_list(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    # todo: user activation
    def test_user_profile_api_response_content(self):
        cnt = 3
        mommy.make(User, cnt)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertIn('email', content.keys())
        self.assertIn('first_name', content.keys())
        self.assertIn('last_name', content.keys())
        self.assertIn('mobile', content.keys())
        self.assertIn('is_active', content.keys())
        self.assertIn('pk', content.keys())

    def test_user_update_api_with_patch(self):
        user = mommy.make(User)
        data = {'is_active': True}
        url = f'{self.url}{user.pk}/'
        resp = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

    def test_user_update_api_with_put(self):
        user = mommy.make(User)
        data = {}
        resp = self.client.put(f'{self.url}{user.pk}/', data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 400)
