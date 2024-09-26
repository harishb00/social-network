from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest, BlockedUser


UserModel = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["id", "status", "sender", "receiver", "created_at"]

    def validate(self, data):
        sender = data["sender"]
        receiver = data["receiver"]

        is_blocked = (
            len(BlockedUser.objects.filter(blocked=sender, blocker=receiver)) > 0
        )
        if is_blocked:
            raise serializers.ValidationError(f"{receiver.username} has blocked you.")
        if sender == receiver:
            raise serializers.ValidationError("sender and receiver can't be same.")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["sender"] = instance.sender.name
        representation["receiver"] = instance.receiver.name
        representation.pop("created_at")
        return representation


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
