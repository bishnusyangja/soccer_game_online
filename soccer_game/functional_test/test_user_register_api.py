from django.test import TestCase
from model_mommy import mommy
from rest_framework.test import APIClient

from team.models import Team, Player
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
        # content = resp.json()
        # team_list = Team.objects.filter(user_id=content['pk'])
        # self.assertEqual(len(team_list), 1)
        # player_list = Player.objects.filter(team=team_list[0])
        # self.assertEqual(len(player_list), 20)

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