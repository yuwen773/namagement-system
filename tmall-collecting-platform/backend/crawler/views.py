"""
Views for crawler module.
爬虫模块的 API 视图 - 简化版（移除 Celery 依赖）
"""
import logging
from typing import Optional

from django.db import connections
from django.db.models import Avg, Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from products.models import CrawlLog

from .serializers import (
    CrawlLogSerializer,
    CrawlLogListSerializer,
    CrawlerStartSerializer,
    CrawlerStatsSerializer,
)
from .services import CrawlerService

logger = logging.getLogger('crawler')


class CrawlerStartView(APIView):
    """
    启动爬虫采集任务

    POST /api/crawler/start/
    请求体：{"mode": "demo", "keywords": ["高达", "手办"]}
    响应：{"code": 0, "message": "任务已启动", "task_id": "xxx"}
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """启动爬虫任务"""
        serializer = CrawlerStartSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'code': -1,
                'message': '参数验证失败',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取参数
        mode = serializer.validated_data.get('mode', 'normal')
        keywords = serializer.validated_data.get('keywords')
        max_pages = serializer.validated_data.get('max_pages', 1)

        # 检查是否有正在运行的任务
        running_tasks = CrawlLog.objects.filter(
            status='running'
        ).count()

        if running_tasks > 0:
            return Response({
                'code': -1,
                'message': f'已有 {running_tasks} 个任务正在运行，请等待完成后再启动新任务'
            }, status=status.HTTP_409_CONFLICT)

        # 启动采集任务
        try:
            task_id = CrawlerService.start_crawl(mode=mode, keywords=keywords, max_pages=max_pages)

            logger.info(f"启动爬虫任务: {task_id}, 模式: {mode}")

            return Response({
                'code': 0,
                'message': '任务已启动',
                'data': {
                    'task_id': task_id,
                    'mode': mode,
                    'status': 'running'
                }
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.error(f"启动爬虫任务失败: {e}")
            return Response({
                'code': -1,
                'message': f'启动任务失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrawlerStatusView(APIView):
    """
    查询爬虫任务状态

    GET /api/crawler/status/{task_id}/
    响应：{"code": 0, "data": {"status": "running", "progress": "50%", ...}}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id: str):
        """获取任务状态"""
        try:
            status_data = CrawlerService.get_status(task_id)

            if status_data is None:
                return Response({
                    'code': -1,
                    'message': '任务不存在'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'code': 0,
                'data': status_data
            })

        except Exception as e:
            logger.error(f"获取任务状态失败: {e}")
            return Response({
                'code': -1,
                'message': f'获取状态失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrawlerStopView(APIView):
    """
    停止爬虫任务

    POST /api/crawler/stop/{task_id}/
    响应：{"code": 0, "message": "任务已停止"}
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, task_id: str):
        """停止任务"""
        try:
            # 更新数据库状态
            crawl_log = CrawlLog.objects.filter(task_id=task_id).first()
            if crawl_log and crawl_log.status == 'running':
                crawl_log.status = 'cancelled'
                crawl_log.end_time = timezone.now()
                crawl_log.save()

                logger.info(f"停止爬虫任务: {task_id}")

                return Response({
                    'code': 0,
                    'message': '任务已停止'
                })
            else:
                return Response({
                    'code': -1,
                    'message': '任务不存在或未在运行中'
                }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"停止任务失败: {e}")
            return Response({
                'code': -1,
                'message': f'停止任务失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrawlLogListView(APIView):
    """
    采集日志列表

    GET /api/crawler/logs/?status=success&page=1&page_size=20
    响应：{"code": 0, "data": [...], "total": 100}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取采集日志列表"""
        try:
            queryset = CrawlLog.objects.all().order_by('-created_at')

            # 状态筛选
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            # 模式筛选
            mode_filter = request.query_params.get('mode')
            if mode_filter:
                queryset = queryset.filter(mode=mode_filter)

            # 分页
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            start = (page - 1) * page_size
            end = start + page_size

            total = queryset.count()
            logs = queryset[start:end]

            serializer = CrawlLogListSerializer(logs, many=True)

            return Response({
                'code': 0,
                'data': serializer.data,
                'total': total
            })

        except Exception as e:
            logger.error(f"获取日志列表失败: {e}")
            return Response({
                'code': -1,
                'message': f'获取日志失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrawlLogDetailView(APIView):
    """
    采集日志详情

    GET /api/crawler/logs/{id}/
    响应：{"code": 0, "data": {...}}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """获取日志详情"""
        try:
            log = CrawlLog.objects.get(id=id)
            serializer = CrawlLogSerializer(log)

            return Response({
                'code': 0,
                'data': serializer.data
            })

        except CrawlLog.DoesNotExist:
            return Response({
                'code': -1,
                'message': '日志不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"获取日志详情失败: {e}")
            return Response({
                'code': -1,
                'message': f'获取详情失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CrawlerStatsView(APIView):
    """
    爬虫统计信息

    GET /api/crawler/stats/
    响应：{"code": 0, "data": {...}}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取爬虫统计信息"""
        try:
            # 基础统计
            total_tasks = CrawlLog.objects.count()
            running_tasks = CrawlLog.objects.filter(status='running').count()
            success_tasks = CrawlLog.objects.filter(status='success').count()
            failed_tasks = CrawlLog.objects.filter(status='failed').count()

            # 计算平均执行时长（秒）
            avg_duration = 0
            completed_logs = CrawlLog.objects.filter(
                status__in=['success', 'failed', 'cancelled'],
                start_time__isnull=False,
                end_time__isnull=False
            )

            if completed_logs.exists():
                total_duration = 0
                for log in completed_logs:
                    delta = log.end_time - log.start_time
                    total_duration += delta.total_seconds()
                avg_duration = total_duration / completed_logs.count()

            # 最近任务
            recent_logs = CrawlLog.objects.all().order_by('-created_at')[:5]
            recent_logs_data = CrawlLogListSerializer(recent_logs, many=True).data

            # 计算总采集数量
            total_items = 0
            for log in CrawlLog.objects.all():
                total_items += log.items_collected

            response_data = {
                'total_tasks': total_tasks,
                'running_tasks': running_tasks,
                'success_tasks': success_tasks,
                'failed_tasks': failed_tasks,
                'total_items_collected': total_items,
                'average_duration': round(avg_duration, 2),
                'recent_logs': recent_logs_data,
            }

            return Response({
                'code': 0,
                'data': response_data
            })

        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return Response({
                'code': -1,
                'message': f'获取统计失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SystemHealthView(APIView):
    """
    系统健康检查

    GET /api/crawler/system-health/
    响应：{"code": 0, "data": {...}}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取系统运行状态"""
        try:
            # 检查数据库连接
            db_status = 'normal'
            try:
                connections['default'].ensure_connection()
            except Exception as e:
                db_status = 'error'
                logger.error(f"数据库连接检查失败: {e}")

            # 检查爬虫服务状态
            running_tasks = CrawlLog.objects.filter(status='running').count()
            crawler_status = 'running' if running_tasks > 0 else 'idle'

            # 获取上次采集时间
            last_crawl = CrawlLog.objects.order_by('-created_at').first()
            last_crawl_time = last_crawl.created_at if last_crawl else None

            # 转换为中国时区并格式化
            if last_crawl_time:
                if timezone.is_naive(last_crawl_time):
                    last_crawl_time = timezone.make_aware(last_crawl_time)
                last_crawl_time_str = timezone.localtime(last_crawl_time).strftime('%Y-%m-%d %H:%M:%S')
            else:
                last_crawl_time_str = None

            response_data = {
                'database': db_status,
                'crawler': crawler_status,
                'active_tasks': running_tasks,
                'last_crawl_time': last_crawl_time_str
            }

            return Response({
                'code': 0,
                'data': response_data
            })

        except Exception as e:
            logger.error(f"获取系统状态失败: {e}")
            return Response({
                'code': -1,
                'message': f'获取系统状态失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
