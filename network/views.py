from django.db.models import Q
from rest_framework import (
    generics as rest_generics,
    viewsets as rest_viewsets,
)

from network import (
    models as network_models,
    serializers as network_serializers
)


class FriendRequestViewSet(rest_viewsets.ModelViewSet):
    model = network_models.FriendRequest
    serializer_class = network_serializers.FriendRequestSerializer

    def get_queryset(self):
        return self.model.objects.filter(
            recipient_id=self.request.user.id,
            status=self.model.STATUS.PENDING
        )
    

class FriendListAPIView(rest_generics.ListAPIView):
    serializer_class = network_serializers.UserFriendSerializer

    def get_queryset(self):
        return network_models.UserFriend.objects.filter(
            user_id=self.request.user.id
        ).order_by('-created_at')
