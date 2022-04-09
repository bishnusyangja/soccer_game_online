import random

import names
from django.conf import settings
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
        team_name += " ", + random.choice(settings.countries)
    team_name += " Club"
    return team_name


def create_team(user):
    team_name = get_random_team_name()
    team = Team(
        name = team_name,
        country = random.choice(settings.countries),
        user = user,
        value = DEFAULT_TEAM_VALUE
    )
    team.save()
    [Player(
        first_name = names.get_first_name(),
        last_name = names.get_last_name(),
        age = random.choice(range(18, 40)),
        country = random.choice(settings.countries),
        position = PLAYER_POSITION[i],
        value = DEFAULT_PLAYER_VALUE,
        team = team
    )
     for i in range(TEAM_MEMBERS)]