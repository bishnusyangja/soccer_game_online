from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from team.models import Player, Team, PlayerMarket
from users.models import User


class PlayerAPITestCase(TestCase):
    client = APIClient()
    url = '/market-player/'

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
        resp = self.client.post(self.url)

    def test_player_market_create_with_empty_data(self):
        data = {}
        resp = self.client.post(self.url, data=data)
        self.assertEqual(resp.status_code, 400)

    def test_player_market_create_with_valid_data(self):
        player = mommy.make(Player, team=self.team)
        data = {'price_value': 100, 'player_id': player.pk}
        resp = self.client.post(self.url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        content = resp.json()
        self.assertIn('player', content)
        self.assertIn('pk', content)
        self.assertIn('team', content)
        self.assertIn('created_on', content)
        self.assertIn('price_value', content)

    def test_player_list_api_response_content(self):
        player_num = 5
        players = mommy.make(Player, player_num, team=self.team, )
        _ = [mommy.make(PlayerMarket, team=self.team, player=player, price_value=500) for player in players]
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content['count'], player_num)
        results = content['results']
        self.assertIn('player', results[0].keys())
        self.assertIn('price_value', results[0].keys())
        self.assertIn('team', results[0].keys())
        self.assertIn('pk', results[0].keys())

    def test_player_market_update_api_with_patch(self):
        player = mommy.make(Player, team=self.team)
        player_2 = mommy.make(Player, team=self.team)
        market = mommy.make(PlayerMarket, player=player, team=self.team)
        data = {'price_value': 500, 'player_id': player_2.pk}
        url = f'{self.url}{market.pk}/'
        resp = self.client.patch(url, data=data, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        content = resp.json()
        self.assertEqual(content['price_value'], data['price_value'])
        self.assertEqual(content['player']['pk'], data['player_id'])

    def test_player_market_destroy(self):
        player = mommy.make(Player, team=self.team)
        market = mommy.make(PlayerMarket, player=player, team=self.team)
        url = f'{self.url}{market.pk}/'
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)

