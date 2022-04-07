from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

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
