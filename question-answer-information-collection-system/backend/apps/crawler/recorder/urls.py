"""
录制爬虫 URL 配置
"""
from django.urls import path
from . import views

app_name = 'recorder'

urlpatterns = [
    # 录制相关
    path('start/', views.start_recording, name='start_recording'),
    path('stop/', views.stop_recording, name='stop_recording'),
    path('steps/', views.get_recording_steps, name='get_steps'),

    # 配置相关
    path('configs/', views.list_configs, name='list_configs'),
    path('config/', views.get_config, name='get_config'),
    path('config/create/', views.create_config, name='create_config'),
    path('config/save/', views.save_config, name='save_config'),
    path('config/delete/', views.delete_config, name='delete_config'),

    # 任务相关
    path('tasks/', views.list_tasks, name='list_tasks'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<str:task_id>/', views.get_task_status, name='get_task_status'),
    path('task/<str:task_id>/start/', views.start_task, name='start_task'),
    path('task/<str:task_id>/pause/', views.pause_task, name='pause_task'),
    path('task/<str:task_id>/resume/', views.resume_task, name='resume_task'),
    path('task/<str:task_id>/stop/', views.stop_task, name='stop_task'),
]
