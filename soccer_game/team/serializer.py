from rest_framework import serializers

from soccer_game.helpers import DateTimeSerializer
from team.models import Player, Team, PlayerMarket


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


class PlayerMarketSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    team = serializers.DictField(source='get_team', read_only=True)
    player = serializers.DictField(read_only=True, source='get_player')
    player_id = serializers.IntegerField()
    created_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')

    def validate_player_id(self, value):
        if not Player.objects.filter(team__user=self.user, pk=value).count():
            raise serializers.ValidationError(f'{value} is not valid player id')
        return value

    class Meta:
        model = PlayerMarket
        read_only_fields = ('description', )
        fields = ('pk', 'player', 'player_id', 'team', 'created_on', 'price_value', 'description', )

    def create(self, validated_data):
        validated_data['team'] = self.context.get('team')
        return super().create(validated_data)