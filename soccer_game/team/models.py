from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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
    price_value = models.IntegerField()

    created_on = models.DateTimeField(_('Created on'), default=timezone.now)
    modified_on = models.DateTimeField(_('Modified on'))

    def __str__(self):
        return self.name

    def get_value(self):
        return "$ {}".format(str(self.price_value))

    def team_value(self):
        player_price = sum([player.value for player in self.players.all()])
        return self.price_value + player_price

    def get_team_value(self):
        return "$ {}".format(str(self.team_value()))

    def get_user(self):
        return {'pk': self.user_id, 'name': self.user.name}

    def save(self, *args, **kwargs):
        self.modified_on = timezone.now()
        super().save(*args, **kwargs)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=50)
    position = models.CharField(max_length=20, choices=POSITION_LIST)
    team = models.ForeignKey(Team, related_name="players", on_delete=models.PROTECT)
    price_value = models.IntegerField()

    created_on = models.DateTimeField(_('Created on'), default=timezone.now)
    modified_on = models.DateTimeField(_('Modified on'))

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_value(self):
        return "$ {}".format(str(self.value))

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.modified_on = timezone.now()
        super().save(*args, **kwargs)

    def get_team(self):
        return {"pk": self.team.pk, "name": self.team.name}


class PlayerMarket(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="market_history")
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="market_history")
    price_value = models.IntegerField()

    created_on = models.DateTimeField(_('Created on'), default=timezone.now)
    modified_on = models.DateTimeField(_('Modified on'))

    def __str__(self):
        return "{} -- {}".format(self.player.get_full_name(), self.team.name)

    def save(self, *args, **kwargs):
        self.modified_on = timezone.now()
        super().save(*args, **kwargs)

