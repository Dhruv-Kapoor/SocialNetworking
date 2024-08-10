from django.contrib.auth import get_user_model
from rest_framework import (
    exceptions as rest_exceptions,
    serializers as rest_serializers
)
from rest_framework.authentication import authenticate
from rest_framework.authtoken import models as rest_auth_models


class UserSignupSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for user signup.
    Creates user object using first name, last name, email and password from payload
    """
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class UserLoginSerializer(rest_serializers.ModelSerializer):
    
    email = rest_serializers.EmailField(write_only=True)
    auth_token = rest_serializers.SerializerMethodField()

    def get_auth_token(self, user):
        token, _ = rest_auth_models.Token.objects.get_or_create(user_id=user.id)
        return token.key

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise rest_exceptions.AuthenticationFailed()

        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'auth_token')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
