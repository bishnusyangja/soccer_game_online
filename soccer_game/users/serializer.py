from rest_framework import serializers

from soccer_game.helpers import DateTimeSerializer
from users.models import User



class UserSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', read_only=True)
    modified_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context.get('http_method')
        if not method or not method.lower() == "post":
            self.fields['email'].read_only = True

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'mobile', 'created_on', 'modified_on', )