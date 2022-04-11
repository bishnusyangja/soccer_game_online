from rest_framework import mixins
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from team.models import Team, Player
from team.serializer import TeamSerializer, PlayerSerializer


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