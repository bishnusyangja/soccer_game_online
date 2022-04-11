import pytz
from django.conf import settings
from rest_framework import serializers

from users.models import User


def get_local_time(value):
    lc_time = pytz.timezone(settings.TIME_ZONE)
    value = value.astimezone(lc_time)
    return value


class DateTimeSerializer(serializers.DateTimeField):

    def to_representation(self, value):
        value = get_local_time(value)
        date = super(DateTimeSerializer, self).to_representation(value)
        return date


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, allow_null=True)
    modified_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context.get('http_method')
        if not method or not method.lower() == "post":
            self.fields['email'].read_only = True

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'mobile', 'created_on', 'modified_on', )