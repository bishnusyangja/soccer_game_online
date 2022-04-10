import random

import names
from django.http import Http404
from rest_framework import mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from soccer_game.permissions import PublicPermission
from team.helpers import create_team
from users.models import User
from users.serializer import UserSerializer


class AppAuthTokenView(ObtainAuthToken):
    authentication_classes = ()


class UserAPIView(
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            GenericViewSet
        ):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.none()

    def get_object(self):
        lookup = self.kwargs.get("pk")
        if lookup == "profile":
            return self.request.user
        raise Http404


class UserRegisterAPIView(mixins.CreateModelMixin,
                   GenericViewSet):
    permission_classes = (PublicPermission, )
    serializer_class = UserSerializer
    queryset = User.objects.none()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            try:
                create_team(request.user)
            except Exception as e:
                print("Exception at Team Creation")
        return response