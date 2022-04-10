from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from users.models import User


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

    # todo: load .env file
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
        data = {'first_name': "Ramesh"}
        url = f'{self.url}profile/'
        resp = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

    def test_user_update_api_with_put(self):
        data = {}
        resp = self.client.put(f'{self.url}profile/', data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 400)
