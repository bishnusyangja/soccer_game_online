from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from users.models import User


class UserAPITestCase(TestCase):
    client = APIClient()
    url = "/user/"

    def setUp(self):
        username = 'bishnu.bhattarai@gmail.com'
        password = '1'
        user = mommy.make(User, email=username, is_staff=True)
        user.set_password(password)
        user.save()
        self.client.login(username=username, password=password)

    def test_user_profile_api_response_content(self):
        resp = self.client.get(f'{self.url}profile/')
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertIn('email', content.keys())
        self.assertIn('first_name', content.keys())
        self.assertIn('last_name', content.keys())
        self.assertIn('mobile', content.keys())
        self.assertIn('created_on', content.keys())
        self.assertIn('modified_on', content.keys())
        self.assertIn('pk', content.keys())

    def test_user_update_api_with_patch(self):
        first_name = "Ramesh"
        last_name = "Adhikari"
        data = {'first_name': first_name, "last_name": last_name}
        url = f'{self.url}profile/'
        resp = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content["first_name"], first_name)
        self.assertEqual(content["last_name"], last_name)

    def test_user_update_api_with_put(self):
        data = {}
        resp = self.client.put(f'{self.url}profile/', data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 400)
