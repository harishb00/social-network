from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import FriendRequest, BlockedUser


class FriendTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="user1",
            email="user1@email.com",
            password="secret",
        )
        cls.user2 = get_user_model().objects.create_user(
            username="user2",
            email="user2@email.com",
            password="secret",
        )
        cls.user3 = get_user_model().objects.create_user(
            username="user3",
            email="user3@email.com",
            password="secret",
        )
        cls.friend_pending = FriendRequest.objects.create(
            sender=cls.user1,
            receiver=cls.user2,
        )
        cls.friend_reject = FriendRequest.objects.create(
            sender=cls.user1, receiver=cls.user3, status="rejected"
        )
        cls.block1 = BlockedUser.objects.create(
            blocker=cls.user1,
            blocked=cls.user2,
        )

    def test_friend_request_model(self):
        self.assertEqual(self.friend_pending.sender.username, "user1")
        self.assertEqual(self.friend_pending.receiver, self.user2)
        self.assertEqual(str(self.friend_pending), "user1 -> user2 (pending)")
        self.assertEqual(str(self.friend_reject), "user1 -> user3 (rejected)")

    def test_blocked_user_model(self):
        self.assertEqual(self.block1.blocker, self.user1)
        self.assertEqual(self.block1.blocked, self.user2)
        self.assertEqual(str(self.block1), "user1 blocked user2")
