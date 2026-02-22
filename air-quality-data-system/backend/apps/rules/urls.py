from django.urls import path

from .views import ProtectionGuideView, ProtectionRuleManageView

urlpatterns = [
    path("protection-guide/", ProtectionGuideView.as_view(), name="protection-guide"),
    path("admin/rules/", ProtectionRuleManageView.as_view(), name="admin-protection-rule-manage"),
]
