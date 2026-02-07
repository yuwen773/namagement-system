"""
爬虫状态 API 视图

提供前端调用的爬虫控制接口，实时反馈状态。
支持启动、停止、查询状态和获取日志。
"""

import json
import redis
from datetime import datetime
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from apps.crawler.tasks import (
    run_spider_task,
    get_task_status,
    get_task_progress,
    get_task_logs,
    stop_spider,
    get_resume_info,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_KEY_PREFIX,
)
from apps.crawler.models import Question
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


def get_redis_client():
    """获取 Redis 客户端"""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def make_response(code=0, data=None, message=None, total=None):
    """构建统一的 API 响应格式"""
    response_data = {
        "code": code,
        "message": message or ("success" if code == 0 else "error"),
    }
    if data is not None:
        response_data["data"] = data
    if total is not None:
        response_data["total"] = total
    return response_data


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限：仅管理员可写，普通用户可读
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class CrawlerStatusView(APIView):
    """
    爬虫状态 API

    提供爬虫任务的状态查询和控制接口。
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取当前爬虫状态

        GET /api/crawler/status/

        响应示例:
        {
            "code": 0,
            "data": {
                "task_id": "abc123",
                "status": "running",
                "progress": 45,
                "collected": 9000,
                "total": 10000,
                "start_time": "2026-02-07T10:30:00",
                "message": "正在采集第 90 页..."
            }
        }
        """
        try:
            redis_client = get_redis_client()

            # 获取所有活跃任务
            pattern = f'{REDIS_KEY_PREFIX}status:*'
            active_tasks = []

            for key in redis_client.scan_iter(match=pattern):
                task_data = redis_client.get(key)
                if task_data:
                    task_info = json.loads(task_data)
                    if task_info.get('status') in ['running', 'pending']:
                        active_tasks.append(task_info)

            # 获取当前运行的任务（如果有）
            current_task = None
            if active_tasks:
                # 返回最新的运行任务
                current_task = max(active_tasks, key=lambda x: x.get('start_time', ''))

            # 获取断点信息
            resume_info = get_resume_info('full')

            response_data = {
                "has_active_task": current_task is not None,
                "current_task": current_task,
                "resume_available": resume_info.get('has_resume', False),
                "resume_info": resume_info if resume_info.get('has_resume') else None,
            }

            return Response(
                make_response(code=0, data=response_data),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"获取状态失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerStartView(APIView):
    """
    启动爬虫任务 API

    POST /api/crawler/start/

    请求参数:
    {
        "mode": "demo" | "full",  // 采集模式
        "limit": 20,              // 采集数量限制
        "api_only": false,        // 是否使用纯API模式
        "resume": false           // 是否断点续传
    }

    响应示例:
    {
        "code": 0,
        "data": {
            "task_id": "abc123-uuid",
            "status": "pending",
            "message": "任务已提交，请稍后查询状态"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request):
        try:
            # 权限检查：仅管理员可启动爬虫
            if not hasattr(request.user, 'role') or request.user.role != 'admin':
                return Response(
                    make_response(code=403, message="仅管理员可以启动爬虫任务"),
                    status=status.HTTP_403_FORBIDDEN
                )

            # 获取请求参数
            mode = request.data.get('mode', 'demo')
            limit = int(request.data.get('limit', 20))
            api_only = request.data.get('api_only', False)
            resume = request.data.get('resume', False)

            # 参数验证
            if mode not in ['demo', 'full']:
                return Response(
                    make_response(code=400, message="无效的采集模式，仅支持 'demo' 或 'full'"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if limit < 1 or limit > 50000:
                return Response(
                    make_response(code=400, message="采集数量应在 1-50000 之间"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 检查是否有正在运行的任务
            redis_client = get_redis_client()
            pattern = f'{REDIS_KEY_PREFIX}status:*'

            for key in redis_client.scan_iter(match=pattern):
                task_data = redis_client.get(key)
                if task_data:
                    task_info = json.loads(task_data)
                    if task_info.get('status') in ['running', 'pending']:
                        return Response(
                            make_response(
                                code=409,
                                message=f"已有任务正在运行 (task_id: {task_info.get('task_id')})",
                                data={"existing_task_id": task_info.get('task_id')}
                            ),
                            status=status.HTTP_409_CONFLICT
                        )

            # 启动 Celery 任务
            task = run_spider_task.delay(
                mode=mode,
                limit=limit,
                api_only=api_only,
                resume=resume
            )

            # 记录启动日志
            log_entry = {
                "timestamp": timezone.now().isoformat(),
                "action": "start",
                "mode": mode,
                "limit": limit,
                "user_id": request.user.id,
                "task_id": task.id,
            }

            log_key = f'{REDIS_KEY_PREFIX}operation_logs'
            redis_client.lpush(log_key, json.dumps(log_entry, ensure_ascii=False))
            redis_client.ltrim(log_key, 0, 99)  # 保留最近100条日志

            return Response(
                make_response(
                    code=0,
                    data={
                        "task_id": task.id,
                        "status": "pending",
                        "mode": mode,
                        "limit": limit,
                        "message": "任务已提交，请稍后查询状态"
                    },
                    message="爬虫任务已启动"
                ),
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"启动任务失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerStopView(APIView):
    """
    停止爬虫任务 API

    POST /api/crawler/stop/

    请求参数:
    {
        "task_id": "abc123-uuid"  // 可选，不提供则停止所有运行中的任务
    }

    响应示例:
    {
        "code": 0,
        "data": {
            "task_id": "abc123-uuid",
            "status": "stopped",
            "message": "任务已停止"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request):
        try:
            # 权限检查：仅管理员可停止爬虫
            if not hasattr(request.user, 'role') or request.user.role != 'admin':
                return Response(
                    make_response(code=403, message="仅管理员可以停止爬虫任务"),
                    status=status.HTTP_403_FORBIDDEN
                )

            task_id = request.data.get('task_id')

            if not task_id:
                # 如果没有指定 task_id，查找正在运行的任务
                redis_client = get_redis_client()
                pattern = f'{REDIS_KEY_PREFIX}status:*'

                running_task_id = None
                for key in redis_client.scan_iter(match=pattern):
                    task_data = redis_client.get(key)
                    if task_data:
                        task_info = json.loads(task_data)
                        if task_info.get('status') == 'running':
                            running_task_id = task_info.get('task_id')
                            break

                if not running_task_id:
                    return Response(
                        make_response(code=404, message="没有正在运行的爬虫任务"),
                        status=status.HTTP_404_NOT_FOUND
                    )

                task_id = running_task_id

            # 调用 Celery 停止任务
            result = stop_spider(task_id)

            return Response(
                make_response(
                    code=0,
                    data=result,
                    message="爬虫任务已停止"
                ),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"停止任务失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerProgressView(APIView):
    """
    获取爬虫任务进度 API

    GET /api/crawler/progress/<task_id>/

    响应示例:
    {
        "code": 0,
        "data": {
            "timestamp": "2026-02-07T10:30:00",
            "current_page": 90,
            "collected": 9000,
            "failed": 5,
            "message": "已采集 9000 条数据"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        try:
            progress = get_task_progress(task_id)

            return Response(
                make_response(code=0, data=progress),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"获取进度失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerLogsView(APIView):
    """
    获取爬虫任务日志 API

    GET /api/crawler/logs/<task_id>/

    响应示例:
    {
        "code": 0,
        "data": {
            "task_id": "abc123-uuid",
            "logs": "2026-02-07 10:30:00 - 正在采集第 1 页...\n2026-02-07 10:30:05 - 采集完成，共 10 条"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        try:
            logs = get_task_logs(task_id)

            return Response(
                make_response(code=0, data={"task_id": task_id, "logs": logs}),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"获取日志失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerResumeView(APIView):
    """
    获取断点续传信息 API

    GET /api/crawler/resume/

    响应示例:
    {
        "code": 0,
        "data": {
            "mode": "full",
            "has_resume": true,
            "last_page": 90,
            "last_id": "abc123"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            mode = request.query_params.get('mode', 'full')
            resume_info = get_resume_info(mode)

            return Response(
                make_response(code=0, data=resume_info),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"获取断点信息失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerOperationLogsView(APIView):
    """
    获取爬虫操作日志 API

    GET /api/crawler/operation-logs/

    响应示例:
    {
        "code": 0,
        "data": [
            {"timestamp": "...", "action": "start", "mode": "demo", ...},
            {"timestamp": "...", "action": "stop", ...}
        ],
        "total": 10
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            redis_client = get_redis_client()
            log_key = f'{REDIS_KEY_PREFIX}operation_logs'

            logs = redis_client.lrange(log_key, 0, 99)
            parsed_logs = []

            for log in logs:
                try:
                    parsed_logs.append(json.loads(log))
                except json.JSONDecodeError:
                    parsed_logs.append({"raw": log})

            # 按时间倒序（最新的在前）
            parsed_logs.reverse()

            return Response(
                make_response(code=0, data=parsed_logs, total=len(parsed_logs)),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"获取操作日志失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IsAdminOrDeleteOnly(permissions.BasePermission):
    """
    自定义权限：所有用户可查看，仅管理员可删除
    未认证时返回 401
    """
    message = "需要登录才能访问"

    def has_permission(self, request, view):
        from rest_framework.exceptions import NotAuthenticated

        if request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS 需要登录
            if not request.user or not request.user.is_authenticated:
                raise NotAuthenticated()
            return True
        # DELETE 需要管理员
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        from rest_framework.exceptions import PermissionDenied

        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        if request.user.role != 'admin':
            raise PermissionDenied("仅管理员可以删除问答")
        return request.user.is_authenticated and request.user.role == 'admin'


class QuestionViewSet(viewsets.ModelViewSet):
    """
    问答数据 API

    提供问答数据的增删改查接口，支持分页、搜索和排序。

    GET /api/questions/          - 获取问答列表（分页）
    GET /api/questions/?search=关键词 - 搜索问答
    GET /api/questions/<id>/     - 获取问答详情
    DELETE /api/questions/<id>/  - 删除问答（仅管理员）
    """
    queryset = Question.objects.prefetch_related('tags').all()
    serializer_class = None  # 在 __init__ 中动态设置
    permission_classes = [IsAdminOrDeleteOnly]

    def __init__(self, *args, **kwargs):
        from apps.api.serializers import QuestionSerializer
        super().__init__(*args, **kwargs)
        self.serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        """
        获取问答列表

        支持参数：
        - page: 页码（默认1）
        - page_size: 每页数量（默认20，最大100）
        - search: 搜索关键词（标题模糊搜索）
        - ordering: 排序字段（默认 -created_at）
        """
        # 获取查询参数
        search = request.query_params.get('search', '')
        ordering = request.query_params.get('ordering', '-created_at')

        # 构建查询集
        queryset = self.get_queryset()

        if search:
            queryset = queryset.filter(title__icontains=search)

        # 排序
        queryset = queryset.order_by(ordering)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = min(int(request.query_params.get('page_size', 20)), 100)

        # 获取总数
        total = queryset.count()

        # 分页查询
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            make_response(
                code=0,
                data=serializer.data,
                total=total
            ),
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        """
        获取问答详情
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            make_response(code=0, data=serializer.data),
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        删除问答（仅管理员）
        """
        instance = self.get_object()
        instance.delete()
        return Response(
            make_response(code=0, message="删除成功"),
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def tags(self, request):
        """
        获取所有标签列表

        GET /api/questions/tags/
        """
        from apps.api.serializers import TagSerializer
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(
            make_response(code=0, data=serializer.data, total=tags.count()),
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """
        获取问答完整详情（包含所有字段）

        GET /api/questions/<id>/detail/
        """
        question = get_object_or_404(Question.objects.prefetch_related('tags'), pk=pk)
        serializer = self.get_serializer(question)
        return Response(
            make_response(code=0, data=serializer.data),
            status=status.HTTP_200_OK
        )
