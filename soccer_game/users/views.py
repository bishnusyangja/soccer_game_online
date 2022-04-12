from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from soccer_game.permissions import PublicPermission
from team.helpers import create_team
from users.models import User
from users.serializer import UserSerializer


class AppAuthTokenView(ObtainAuthToken):
    authentication_classes = ()


class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.none()

    def get_object(self):
        return self.request.user


class UserRegisterAPIView(CreateAPIView):
    permission_classes = (PublicPermission, )
    serializer_class = UserSerializer
    queryset = User.objects.none()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            try:
                create_team(response.data['pk'])
            except Exception as e:
                print("Exception at Team Creation", e)
        return response

    def get_serializer_context(self, *args, **kwargs):
        kwargs = super().get_serializer_context(*args, **kwargs)
        kwargs["http_method"] = self.request.method
        return kwargs