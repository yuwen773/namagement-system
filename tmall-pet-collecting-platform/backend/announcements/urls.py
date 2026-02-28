from django.urls import path
from .views import (
    AnnouncementListView,
    AnnouncementDetailView,
    AdminAnnouncementListView,
    AdminAnnouncementDetailView,
    PublishAnnouncementView,
    UnpublishAnnouncementView
)

urlpatterns = [
    # 普通用户端接口
    path('', AnnouncementListView.as_view(), name='announcement-list'),
    path('<uuid:id>/', AnnouncementDetailView.as_view(), name='announcement-detail'),

    # 管理员端接口
    path('admin/', AdminAnnouncementListView.as_view(), name='admin-announcement-list'),
    path('admin/<uuid:id>/', AdminAnnouncementDetailView.as_view(), name='admin-announcement-detail'),
    path('admin/<uuid:id>/publish/', PublishAnnouncementView.as_view(), name='publish-announcement'),
    path('admin/<uuid:id>/unpublish/', UnpublishAnnouncementView.as_view(), name='unpublish-announcement'),
]
