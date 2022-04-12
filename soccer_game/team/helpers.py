import random

import names
from django.db import transaction
from django.utils import timezone

from soccer_game import settings
from team.models import Team, Player


DEFAULT_PLAYER_VALUE = 1*1000*1000
DEFAULT_TEAM_VALUE = 5*1000*1000
TEAM_MEMBERS = 20
PLAYER_POSITION = ["goal_keeper"]*3 + ["defender"]*6 +["mid_fielder"]*6 + ["attacker"]*5


def get_random_team_name():
    team_name = names.get_last_name()
    if random.choice([0, 1]):
        team_name += " " + names.get_first_name()
    if random.choice([0, 1]):
        team_name += " " + random.choice(settings.countries)
    team_name += " Club"
    return team_name


def create_team(user_id):
    team_name = get_random_team_name()
    team = Team(
        name = team_name,
        country = random.choice(settings.countries),
        user_id = user_id,
        price_value = DEFAULT_TEAM_VALUE
    )
    team.save()
    bulk_obj = [Player(
        first_name = names.get_first_name(),
        last_name = names.get_last_name(),
        age = random.choice(range(18, 40)),
        country = random.choice(settings.countries),
        position = PLAYER_POSITION[i],
        price_value = DEFAULT_PLAYER_VALUE,
        team = team,
        modified_on = timezone.now()
    )
     for i in range(TEAM_MEMBERS)]
    Player.objects.bulk_create(bulk_obj)


def get_player_value(player):
    return int(player.price_value * random.choice(range(10, 100)))


def upgrade_player_value_and_team(player, team):
    player.team = team
    player.price_value = get_player_value(player)
    player.save()
    return player.price_value


def deduct_new_team_value(team, price_value):
    team -= price_value
    team.save()


def increase_old_team_value(team, price_value):
    team.price_value += price_value
    team.save()


def is_player_affordable(team, price_value):
    return team.price_value >= price_value


def transfer_player_to_team(player_market, team):
    with transaction.atomic():
        player = Player.objects.select_for_update().get(pk=player_market.player.id)
        old_team = Team.objects.select_for_update().get(pk=player_market.team.pk)
        team = Team.objects.select_for_update().get(pk=team.pk)
        upgrade_player_value_and_team(player, team)
        price_value = player_market.price_value
        deduct_new_team_value(team, price_value)
        increase_old_team_value(old_team, price_value)
        return player

