from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'bio', 'description', 'username', 'role')
        read_only_fields = ('id',)


class AuthDataSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.IntegerField()
    username = serializers.CharField(max_length=256)
