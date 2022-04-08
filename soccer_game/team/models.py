from django.db import models

from users.models import User

POSITION_LIST = (
    ("goal_keeper", "GOAL_KEEPER"), # 3
    ("defender", "DEFENDER"),  # 6
    ("mid_fielder", "MID_FIELDER"), # 6
    ("attacker", "ATTACKER"), # 5
)


class Team(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    user = models.OneToOneField(User, null=True, on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return self.name

    def get_value(self):
        return "$ {}".format(str(self.value))

    def team_value(self):
        player_value = sum([player.value for player in self.players.all()])
        return self.value + player_value

    def get_team_value(self):
        return "$ {}".format(str(self.team_value()))

    def get_user(self):
        return {'pk': self.user.pk, 'name': self.user.name}


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=50)
    position = models.CharField(max_length=20, choices=POSITION_LIST)
    team = models.ForeignKey(Team, related_name="players", on_delete=models.PROTECT)
    value = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_value(self):
        return "$ {}".format(str(self.value))