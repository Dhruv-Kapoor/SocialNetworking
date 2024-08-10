from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
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

        value = value.lower()

        sq = SearchQuery('')
        bits = smart_split(value)
        for bit in bits:
            sq |= SearchQuery(bit)
        
        return qs.annotate(
            sv=SearchVector('first_name', 'last_name')
        ).filter(
            Q(email=value) | Q(sv__icontains=sq)
        )

