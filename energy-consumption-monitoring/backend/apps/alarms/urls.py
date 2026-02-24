from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.alarms.views import AlarmRuleViewSet, AlarmViewSet

router = DefaultRouter()
router.register("alarm-rules", AlarmRuleViewSet, basename="alarm-rule")
router.register("alarms", AlarmViewSet, basename="alarm")

urlpatterns = [
    path("", include(router.urls)),
]
