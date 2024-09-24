from django.urls import path

from .views import (
    RequestListView,
    Request,
    Accept,
    Reject,
    block,
    UnBlock,
    list_my_friends,
)

urlpatterns = [
    path("request/", RequestListView.as_view(), name="pending_request"),
    path("request/<int:pk>/", Request.as_view(), name="send_request"),
    path("accept/<int:pk>/", Accept.as_view(), name="accept"),
    path("reject/<int:pk>/", Reject.as_view(), name="reject"),
    path("block/<int:user_id>/", block, name="block"),
    path("unblock/<int:user_id>/", UnBlock.as_view(), name="unblock"),
    path("", list_my_friends, name="list"),
]
