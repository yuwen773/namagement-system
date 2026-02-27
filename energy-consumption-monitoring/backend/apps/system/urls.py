from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.system.views import (
    AdminNoticeViewSet,
    AdminTipsViewSet,
    NoticeViewSet,
    OperationLogViewSet,
    ProfileViewSet,
    RoleViewSet,
    TipsViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("roles", RoleViewSet, basename="role")
router.register("notices", NoticeViewSet, basename="notice")
router.register("tips", TipsViewSet, basename="tip")
router.register("admin/notices", AdminNoticeViewSet, basename="admin-notice")
router.register("admin/tips", AdminTipsViewSet, basename="admin-tip")
router.register("logs", OperationLogViewSet, basename="log")

profile_view = ProfileViewSet.as_view(
    {
        "get": "retrieve_profile",
        "put": "update_profile",
    }
)
profile_bind_rooms_view = ProfileViewSet.as_view({"get": "bind_rooms", "post": "bind_rooms", "delete": "bind_rooms"})
profile_alarm_subscriptions_view = ProfileViewSet.as_view(
    {
        "get": "alarm_subscriptions",
        "put": "alarm_subscriptions",
    }
)
profile_balance_view = ProfileViewSet.as_view({"get": "balance"})

urlpatterns = [
    path("", include(router.urls)),
    path("profile/", profile_view, name="profile"),
    path("profile/bind-rooms/", profile_bind_rooms_view, name="profile-bind-rooms"),
    path(
        "profile/alarm-subscriptions/",
        profile_alarm_subscriptions_view,
        name="profile-alarm-subscriptions",
    ),
    path("profile/balance/", profile_balance_view, name="profile-balance"),
]
