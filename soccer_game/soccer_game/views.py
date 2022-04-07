from rest_framework.renderers import CoreJSONRenderer
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework_swagger.views import get_swagger_view

from soccer_game.permissions import StaffPermission


class SwaggerView(APIView):
    permission_classes = (StaffPermission,)
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request, *args, **kwargs):
        response = get_swagger_view(title='Soccer Game API').view_class().get(request)
        return response