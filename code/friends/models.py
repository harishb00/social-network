from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

UserModel = get_user_model()


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    sender = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="sent_requests",
    )
    receiver = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="received_requests",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["sender", "receiver"], name="unique_sender_receiver"
            ),
        ]

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"


class BlockedUser(models.Model):
    blocker = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="blocker",
    )
    blocked = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="blocked",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
