"""soccer_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from soccer_game.views import SwaggerView
from team.views import TeamAPIView, PlayerAPIView, PlayerMarketAPIView
from users.views import UserAPIView, AppAuthTokenView, UserRegisterAPIView

router = DefaultRouter()


router.register(r'player', PlayerAPIView)
router.register(r'market-player', PlayerMarketAPIView)



urlpatterns = [
    path('soc-admin/', admin.site.urls),
    path('user/profile/', UserAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('team/', TeamAPIView.as_view()),
    path('login/', AppAuthTokenView.as_view()),
    path('docs/sw-api/', SwaggerView.as_view())

]

urlpatterns += router.urls
