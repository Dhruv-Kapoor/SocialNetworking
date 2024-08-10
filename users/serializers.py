from django.contrib.auth import get_user_model
from rest_framework import serializers as rest_serializers


class UserSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'full_name', 'email')
