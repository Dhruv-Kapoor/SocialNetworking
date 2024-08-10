from datetime import datetime, timedelta

from django.db import transaction
from rest_framework import (
    exceptions as rest_exceptions,
    serializers as rest_serializers
)

from users import serializers as users_serializers
from network import (
    constants as network_constants,
    models as network_models
)


class FriendRequestSerializer(rest_serializers.ModelSerializer):
    sender = users_serializers.UserSerializer(read_only=True)
    recipient = users_serializers.UserSerializer(read_only=True)
    recipient_id = rest_serializers.IntegerField(write_only=True)

    def validate_recipient_id(self, recipient_id):
        if recipient_id == self.context['request'].user.id:
            raise rest_exceptions.ValidationError(network_constants.ERROR_MESSAGES['SELF_REQUEST'])

        if network_models.FriendRequest.objects.filter(
            sender_id=self.context['request'].user.id,
            recipient_id=recipient_id,
            status__in=[
                network_models.FriendRequest.STATUS.PENDING,
                network_models.FriendRequest.STATUS.ACCEPTED,
            ]
        ).exists():
            raise rest_exceptions.ValidationError(network_constants.ERROR_MESSAGES['REQUEST_ALREADY_EXISTS'])
        
        if network_models.FriendRequest.objects.filter(
            sender_id=self.context['request'].user.id,
            sent_at__gt=datetime.now() - timedelta(minutes=1)
        ).count() >= network_constants.REQUEST_RATE_LIMIT:
            raise rest_exceptions.ValidationError(network_constants.ERROR_MESSAGES['RATE_LIMIT_EXCEEDED'])

        return recipient_id
    
    @transaction.atomic()
    def update(self, instance, validated_data):
        friend_req = super().update(instance, validated_data)
        
        if friend_req.is_accepted:
            user_friend_objs = [
                network_models.UserFriend(
                    user_id=friend_req.sender_id,
                    friend_id=friend_req.recipient_id
                ),
                network_models.UserFriend(
                    user_id=friend_req.recipient_id,
                    friend_id=friend_req.sender_id
                )
            ]
            network_models.UserFriend.objects.bulk_create(user_friend_objs)
            
            network_models.FriendRequest.objects.filter(
                sender_id=friend_req.recipient_id,
                recipient_id=friend_req.sender_id
            ).update(status=network_models.FriendRequest.STATUS.INVALID)

        return friend_req

    @transaction.atomic()
    def create(self, validated_data):
        validated_data['sender_id'] = self.context['request'].user.id
        return super().create(validated_data)

    class Meta:
        model = network_models.FriendRequest
        fields = ('id', 'sender', 'recipient', 'recipient_id', 'status')


class UserFriendSerializer(rest_serializers.Serializer):
    friend = users_serializers.UserSerializer()
    friend_since = rest_serializers.DateTimeField(source='created_at')
