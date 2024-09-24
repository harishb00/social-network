from django.contrib import admin
from .models import FriendRequest, BlockedUser


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = [
        "sender",
        "receiver",
        "status",
        "created_at",
        "updated_at",
    ]


class BlockedUserAdmin(admin.ModelAdmin):
    list_display = [
        "blocker",
        "blocked",
        "created_at",
    ]


admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(BlockedUser, BlockedUserAdmin)
