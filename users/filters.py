from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from django_filters.rest_framework import (
    FilterSet,
    filters as rest_filters
)
from django.utils.text import smart_split


class UsersListFilterSet(FilterSet):
    q = rest_filters.CharFilter(method='search_qs')

    class Meta:
        model = get_user_model()
        fields = ('q',)

    def search_qs(self, qs, name, value):
        if not value:
            return qs

        return qs.annotate(
            user_full_name=Concat(F('first_name'), Value(' '), F('last_name'))
        ).filter(
            Q(email=value.lower()) | Q(user_full_name__icontains=value)
        )

