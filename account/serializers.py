from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name',  'last_name',
                  'is_active', 'password',)
        read_only_fields = ('is_active',)
        extra_kwargs = {'password': {'write_only': True, 'required': False}}


class SignUpSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)

