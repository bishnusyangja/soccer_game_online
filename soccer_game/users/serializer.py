from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'mobile', 'is_active', 'is_staff', 'is_superuser', )