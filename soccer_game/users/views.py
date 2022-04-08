import random

import names
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from team.helpers import create_team
from users.models import User
from users.serializer import UserSerializer


class AppAuthTokenView(ObtainAuthToken):
    authentication_classes = ()


class UserAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(self.request.user.pk)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            try:
                create_team(request.user)
            except Exception as e:
                print("Exception at Team Creation")
        return response
