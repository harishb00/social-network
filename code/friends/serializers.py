from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest, BlockedUser


UserModel = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = "__all__"

    def get_sender_name(self, obj):
        return obj.sender.name

    def get_receiver_name(self, obj):
        return obj.receiver.name

    def validate(self, data):
        sender = data["sender"]
        receiver = data["receiver"]

        is_blocked = (
            len(BlockedUser.objects.filter(blocked=sender, blocker=receiver)) > 0
        )
        if is_blocked:
            raise serializers.ValidationError(f"{receiver.username} has blocked you.")

        return data


class FriendDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ["user_id", "username", "name"]

    def get_user_id(self, obj):
        return obj.id


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = "__all__"
