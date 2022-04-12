from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from team.helpers import is_player_affordable, transfer_player_to_team
from team.models import Team, Player, PlayerMarket
from team.serializer import TeamSerializer, PlayerSerializer, PlayerMarketSerializer


class TeamAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TeamSerializer
    queryset = Team.objects.none()

    def get_object(self):
        return Team.objects.get(user=self.request.user)


class PlayerAPIView(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PlayerSerializer
    queryset = Player.objects.none()

    def get_queryset(self):
        return Player.objects.filter(team__user=self.request.user)


class PlayerMarketAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayerMarketSerializer
    queryset = PlayerMarket.objects.none()

    def get_queryset(self):
        return PlayerMarket.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        kwargs = super().get_serializer_context(*args, **kwargs)
        kwargs['team'] = Team.objects.get(user=self.request.user)
        kwargs['user'] = self.request.user
        return kwargs

    @action(detail=True, methods=['POST'])
    def buy(self, request, pk):
        price_value_from_team = request.data.get('price_value')
        team = request.user.team
        player_market = self.get_object()
        if price_value_from_team != player_market.price_value:
            print('at price')
            return Response({'error': 'Price mismatch'}, status=400)
        if not is_player_affordable(team, player_market.price_value):
            print("at affordable")
            return Response({'error': 'You can not afford this player'}, status=400)
        try:
            player = transfer_player_to_team(player_market, team)
            data = {'team': {'pk': player.team.pk, 'name': player.team.name},
                        'player': {'pk': player.pk, 'price_value': player.price_value, 'name': player.get_full_name()}}
            return Response(data, status=200)
        except Exception as e:
            print("PlayerTransfer ", e)
            data = {'error': 'Something went wrong. Try again later.'}
            return Response(data, status=500)
