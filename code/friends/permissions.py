from rest_framework import permissions


class IsAuthorizedToAcceptOrReject(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # only the receiver can accept the pending request
        return obj.receiver == request.user


class IsAuthorizedToUnblock(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # only the receiver can accept the pending request
        return obj.blocker == request.user
