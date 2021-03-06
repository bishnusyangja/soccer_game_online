from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from team.models import Player, Team
from users.models import User


class PlayerAPITestCase(TestCase):
    # for patch and put request this APIClient needs content_type="application/json"
    client = APIClient()
    url = '/team/'

    def setUp(self):
        username = 'bishnu.bhattarai@gmail.com'
        password = '1'
        self.user = mommy.make(User, email=username, is_staff=True)
        self.user.set_password(password)
        self.user.save()
        self.team = mommy.make(Team, user=self.user)
        self.client.login(username=username, password=password)

    def test_team_retrieve(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertIn('pk', content)
        self.assertIn('name', content)
        self.assertIn('country', content)
        self.assertIn('user', content)
        self.assertIn('price_value', content)

    def test_team_update(self):
        data = {'name': 'ABC', 'country': 'XYZ'}
        resp = self.client.patch(self.url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content['name'], data['name'])
        self.assertEqual(content['country'], data['country'])