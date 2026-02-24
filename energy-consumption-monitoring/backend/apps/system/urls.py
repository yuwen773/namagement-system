from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.system.views import (
    AdminNoticeViewSet,
    BillViewSet,
    NoticeViewSet,
    OperationLogViewSet,
    ProfileViewSet,
    RechargeViewSet,
    RoleViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("roles", RoleViewSet, basename="role")
router.register("bills", BillViewSet, basename="bill")
router.register("notices", NoticeViewSet, basename="notice")
router.register("admin/notices", AdminNoticeViewSet, basename="admin-notice")
router.register("logs", OperationLogViewSet, basename="log")
router.register("recharges", RechargeViewSet, basename="recharge")

profile_view = ProfileViewSet.as_view(
    {
        "get": "retrieve_profile",
        "put": "update_profile",
    }
)
profile_bind_rooms_view = ProfileViewSet.as_view({"post": "bind_rooms", "delete": "bind_rooms"})
profile_alarm_subscriptions_view = ProfileViewSet.as_view(
    {
        "get": "alarm_subscriptions",
        "put": "alarm_subscriptions",
    }
)

urlpatterns = [
    path("", include(router.urls)),
    path("profile/", profile_view, name="profile"),
    path("profile/bind-rooms/", profile_bind_rooms_view, name="profile-bind-rooms"),
    path(
        "profile/alarm-subscriptions/",
        profile_alarm_subscriptions_view,
        name="profile-alarm-subscriptions",
    ),
]
