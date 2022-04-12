from rest_framework import serializers

from soccer_game.helpers import DateTimeSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', read_only=True)
    modified_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, allow_null=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        method = self.context.get('http_method')
        is_password = self.context.get('is_password')
        if not method or not method.lower() == "post":
            self.fields['email'].read_only = True
        if not is_password:
            self.fields.pop('password')

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'mobile', 'created_on', 'modified_on', 'password', )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
