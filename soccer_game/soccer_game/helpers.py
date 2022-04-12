import pytz
from rest_framework import serializers

from soccer_game import settings


def get_local_time(value):
    lc_time = pytz.timezone(settings.TIME_ZONE)
    value = value.astimezone(lc_time)
    return value


class DateTimeSerializer(serializers.DateTimeField):

    def to_representation(self, value):
        value = get_local_time(value)
        date = super(DateTimeSerializer, self).to_representation(value)
        return date
