from rest_framework import serializers

from team.models import Player, Team


class PlayerSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    team = serializers.DictField(source='get_team', read_only=True)

    class Meta:
        model = Player
        fields = ('pk', 'first_name', 'last_name', 'country', 'age', 'position', 'team', 'price_value')


class TeamSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.DictField(source='get_user', read_only=True)
    price_value = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ('pk', 'name', 'country', 'user', 'price_value', )