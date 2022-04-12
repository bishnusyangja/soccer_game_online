from rest_framework import mixins
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

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