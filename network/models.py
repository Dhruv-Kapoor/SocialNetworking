from collections import namedtuple
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class FriendRequest(models.Model):
    STATUS = namedtuple('STATUS', ['PENDING', 'ACCEPTED', 'REJECTED', 'INVALID'])(
        PENDING=1,
        ACCEPTED=2,
        REJECTED=3,
        INVALID=4
    )
    STATUS_CHOICES = (
        (STATUS.PENDING, 'Pending'),
        (STATUS.ACCEPTED, 'Accepted'),
        (STATUS.REJECTED, 'Rejected'),
        (STATUS.INVALID, 'Invalid'),
    )

    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_requests')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recieved_requests')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS.PENDING)
    
    sent_at = models.DateTimeField(default=datetime.now)
    action_taken_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_accepted(self):
        return self.status == self.STATUS.ACCEPTED

    def __str__(self) -> str:
        return f'{self.sender} - {self.recipient} - {self.status}'


class UserFriend(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='my_friends')
    friend = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friends_with')

    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self) -> str:
        return f'{self.user} - {self.friend}'
