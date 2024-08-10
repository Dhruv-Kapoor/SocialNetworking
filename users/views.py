from django.contrib.auth import get_user_model
from rest_framework import generics as rest_generics

from users import (
    filters as user_filters,
    serializers as user_serializers
)


class UsersListAPIView(rest_generics.ListAPIView):
    serializer_class = user_serializers.UserSerializer
    filterset_class = user_filters.UsersListFilterSet

    def get_queryset(self):
        return get_user_model().objects.exclude(
            id=self.request.user.id
        ).order_by('first_name', 'last_name')
