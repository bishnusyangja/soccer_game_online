import json

from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from team.models import Player
from users.models import User


class PlayerAPITestCase(TestCase):
    # for patch and put request this APIClient needs content_type="application/json"
    client = APIClient()
    url = '/player/'

    def setUp(self):
        username = 'bishnu.bhattarai@gmail.com'
        password = '1'
        user = mommy.make(User, email=username, is_staff=True)
        user.set_password(password)
        user.save()
        self.client.login(username=username, password=password)

    def test_player_list(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_player_list_api_response_content(self):
        cnt = 3
        mommy.make(User, cnt)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content['count'], cnt+1)
        results = content['results']
        self.assertIn('first_name', results[0].keys())
        self.assertIn('last_name', results[0].keys())
        self.assertIn('country', results[0].keys())
        self.assertIn('pk', results[0].keys())

    def test_player_create_with_no_data(self):
        data = {}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_player_create_with_data(self):
        data = {}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 201)

    def test_player_update_api_with_patch(self):
        user = mommy.make(User)
        data = {'is_active': True}
        url = f'{self.url}{user.pk}/'
        resp = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

    def test_player_update_api_with_put(self):
        user = mommy.make(User)
        data = {}
        resp = self.client.put(f'{self.url}{user.pk}/', data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_player_delete_api(self):
        user = mommy.make(User)
        resp = self.client.delete(f'{self.url}{user.pk}/')
        self.assertEqual(resp.status_code, 204)