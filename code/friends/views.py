from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.db import transaction
from friends.throttles import FriendRequestThrottle


from .permissions import IsAuthorizedToAcceptOrReject, IsAuthorizedToUnblock

from .queries import get_pending_requests, get_my_friends, are_friends
from .serializers import (
    FriendRequestSerializer,
    FriendDetailSerializer,
    BlockSerializer,
)
from .models import FriendRequest, BlockedUser
from datetime import timezone
from datetime import datetime
from django.conf import settings


UserModel = get_user_model()


class RequestPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class Request(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, pk: int):
        self.throttle_classes = [FriendRequestThrottle]

        try:
            receiver = UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            return Response(
                {
                    "error": f"User with id {pk} not found to send request",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        sender = request.user
        if sender == receiver:
            return Response(
                {"error": "You can't send friend request to yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if are_friends(sender, receiver):
            return Response(
                {"error": "You're already friends"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            frs = FriendRequest.objects.select_for_update().filter(
                sender=sender, receiver=receiver
            )
            if not frs:
                # CASE 1: Request is already sent by receiver
                frs = FriendRequest.objects.filter(sender=receiver, receiver=sender)
                if frs:
                    return Response(
                        {
                            "error": f"You already have a friend request from {receiver.name}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                serializer = FriendRequestSerializer(
                    data={
                        "sender": sender.pk,
                        "receiver": receiver.pk,
                    }
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                fr = frs[0]
                # CASE 1: Rejected
                if fr.status == "rejected":
                    if self.is_allowed_to_resend_request(fr):
                        fr.status = "pending"
                        serializer = FriendRequestSerializer(fr)
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        wait_time = self.get_wait_time_for_rejected_requests(fr)
                        return Response(
                            {
                                "error": f"Rejected requests can be resent only after cool down period of {settings.COOL_DOWN_PERIOD} hours. Wait for {wait_time} more hours"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                # CASE 2: Pending
                elif fr.status == "pending":
                    return Response(
                        {"error": "Request is already sent."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

    def is_allowed_to_resend_request(self, friend_request):
        current_time = datetime.now().replace(tzinfo=timezone.utc)
        rejected_time = friend_request.updated_at
        hours_difference = (current_time - rejected_time).total_seconds() / 3600
        return hours_difference > settings.COOL_DOWN_PERIOD

    def get_wait_time_for_rejected_requests(self, friend_request):
        current_time = datetime.now().replace(tzinfo=timezone.utc)
        rejected_time = friend_request.updated_at
        hours_difference = (current_time - rejected_time).total_seconds() / 3600
        return round(settings.COOL_DOWN_PERIOD - hours_difference)


class RequestListView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    pagination_class = RequestPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        return get_pending_requests(self.request.user)


class Accept(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthorizedToAcceptOrReject,)

    def put(self, request: Request, pk: int):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {
                    "error": f"Friend request with id {pk} not found to accept",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, friend_request)

        friend_request.status = "accepted"
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)

        # cache invalidation
        cache_key = f"friends_{request.user.id}"
        cache.delete(cache_key)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Reject(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthorizedToAcceptOrReject,)

    def put(self, request: Request, pk: int):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response(
                {
                    "error": f"Friend request with id {pk} not found to reject",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, friend_request)

        if friend_request.status == "pending":
            friend_request.status = "rejected"
            friend_request.save()
            serializer = FriendRequestSerializer(friend_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Only pending friend requests can be rejected"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def list_my_friends(request: Request):
    user = request.user
    cache_key = f"friends_{user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data)

    my_friends = get_my_friends(user)
    serializer = FriendDetailSerializer(my_friends, many=True)
    response_data = serializer.data
    cache.set(cache_key, response_data, timeout=300)  # 5 minutes
    return Response(response_data)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def block(request: Request, user_id: int):
    blocker = request.user
    blocked_user_id = user_id
    try:
        blocked_user = UserModel.objects.get(pk=blocked_user_id)
    except UserModel.DoesNotExist:
        return Response(
            {
                "error": f"User with id {blocked_user_id} not found to block",
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = BlockSerializer(
        data={
            "blocker": blocker.pk,
            "blocked": blocked_user.pk,
        }
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User blocked successfully."}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnBlock(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthorizedToUnblock,)

    def delete(self, request: Request, user_id: int):
        blocker = request.user
        blocked_user_id = user_id
        try:
            blocked_user = UserModel.objects.get(pk=user_id)
            blocked_record = BlockedUser.objects.get(
                blocker=blocker, blocked=blocked_user
            )
        except UserModel.DoesNotExist:
            return Response(
                {
                    "error": f"User with id {blocked_user_id} does not exist to unblock",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except BlockedUser.DoesNotExist:
            return Response(
                {
                    "error": f"User with id {blocked_user_id} is not blocked",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, blocked_record)
        blocked_record.delete()
        return Response(
            {"message": "User unblocked successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
