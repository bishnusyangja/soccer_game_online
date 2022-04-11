from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from team.models import Player, Team
from users.models import User


class PlayerAPITestCase(TestCase):
    # for patch and put request this APIClient needs content_type="application/json"
    client = APIClient()
    url = '/player/'

    def setUp(self):
        username = 'bishnu.bhattarai@gmail.com'
        password = '1'
        self.user = mommy.make(User, email=username, is_staff=True)
        self.user.set_password(password)
        self.user.save()
        self.team = mommy.make(Team, user=self.user)
        self.client.login(username=username, password=password)

    def test_loggout_out_client(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 401)

    def test_player_list(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_player_list_api_response_content(self):
        player_num = 15
        mommy.make(Player, player_num, team=self.team)
        user_2 = mommy.make(User)
        team_2 = mommy.make(Team, user=user_2)
        mommy.make(Player, 5, team=team_2)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content['count'], player_num)
        results = content['results']
        self.assertIn('first_name', results[0].keys())
        self.assertIn('last_name', results[0].keys())
        self.assertIn('country', results[0].keys())
        self.assertIn('pk', results[0].keys())

    def test_player_update_api_with_patch(self):
        user = mommy.make(Player, team=self.team)
        last_name = "ABC"
        age = 35
        data = {'last_name': last_name, "age": age}
        url = f'{self.url}{user.pk}/'
        resp = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

