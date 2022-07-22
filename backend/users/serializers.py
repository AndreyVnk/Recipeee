from rest_framework import serializers
from users.models import CustomUser
from django.shortcuts import get_object_or_404


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True, read_only=False)
    current_password = serializers.CharField(required=True)

    #class Meta:
    #    model = CustomUser
    #    fields = ('new_password', 'current_password')

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('current_password')):
            raise serializers.ValidationError({'current_password': 'Wrong password.'})
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for users endpoint.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for POST method users endpoint.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {"Wrong username": "User 'me' can not be created."}
            )
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
