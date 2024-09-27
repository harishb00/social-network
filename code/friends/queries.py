from friends.models import FriendRequest
from django.db.models import Q
from django.contrib.auth import get_user_model


UserModel = get_user_model()


def get_pending_requests(user):
    pending_requests = FriendRequest.objects.filter(receiver=user, status="pending")
    return pending_requests


def get_my_friends(user):
    friend_requests = FriendRequest.objects.filter(
        Q(sender=user, status="accepted") | Q(receiver=user, status="accepted")
    ).select_related("sender", "receiver")

    friends = set()
    for request in friend_requests:
        if request.sender == user:
            friends.add(request.receiver)
        else:
            friends.add(request.sender)

    return friends


def are_friends(user1, user2):
    return FriendRequest.objects.filter(
        Q(sender=user1, receiver=user2, status="accepted")
        | Q(sender=user2, receiver=user1, status="accepted")
    ).exists()
