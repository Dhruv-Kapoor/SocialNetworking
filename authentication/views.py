from rest_framework import generics as rest_generics
from rest_framework.permissions import AllowAny

from authentication import serializers as authentication_serializers


class UserSignupAPIView(rest_generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = authentication_serializers.UserSignupSerializer


class UserLoginAPIView(rest_generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = authentication_serializers.UserLoginSerializer
