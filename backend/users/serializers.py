from rest_framework import serializers
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = CustomUser
      fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {"Wrong username": "User 'me' can not be created."}
            )
        return data
