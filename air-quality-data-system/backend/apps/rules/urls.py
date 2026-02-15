from django.urls import path

from .views import ProtectionGuideView

urlpatterns = [
    path("protection-guide/", ProtectionGuideView.as_view(), name="protection-guide"),
]
