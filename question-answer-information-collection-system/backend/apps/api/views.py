"""
爬虫状态 API 视图 (简化版)

提供前端调用的爬虫控制接口，实时反馈状态。
支持启动、停止、查询状态。

简化说明：
- 移除 Celery 依赖，直接使用 subprocess + threading
- 移除 Redis 依赖，使用内存变量存储状态
"""

import json
from datetime import datetime
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from apps.crawler.models import Question, Answer
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDate


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


# 爬虫状态（全局变量，简化版）
_crawler_status = {
    'running': False,
    'mode': None,
    'limit': 0,
    'collected': 0,
    'message': '空闲',
    'start_time': None
}

# 状态文件路径
import os
from pathlib import Path
CRAWLER_STATUS_FILE = Path(__file__).parent.parent.parent / 'apps' / 'crawler' / 'crawler_status.json'


def _save_crawler_status():
    """保存爬虫状态到文件"""
    import json
    try:
        with open(CRAWLER_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(_crawler_status, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存状态失败: {e}")


def _load_crawler_status():
    """从文件加载爬虫状态"""
    import json
    try:
        if CRAWLER_STATUS_FILE.exists():
            with open(CRAWLER_STATUS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _crawler_status.update(data)
    except Exception as e:
        print(f"加载状态失败: {e}")


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
    爬虫状态 API (简化版)

    提供爬虫任务的状态查询接口。
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 每次获取状态时从文件加载最新状态
        _load_crawler_status()

        # 如果任务正在运行，从数据库获取实时进度
        if _crawler_status.get('running'):
            try:
                from apps.crawler.models import Question
                from django.db import connection

                start_time = _crawler_status.get('start_time')
                if start_time:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT COUNT(*) FROM crawler_question WHERE created_at > %s",
                            [start_time]
                        )
                        result = cursor.fetchone()
                        if result:
                            _crawler_status['collected'] = result[0]
            except Exception as e:
                print(f"获取实时进度失败: {e}")

        """
        获取当前爬虫状态

        GET /api/crawler/status/

        响应示例:
        {
            "code": 0,
            "data": {
                "has_active_task": true,
                "mode": "demo",
                "limit": 20,
                "collected": 5,
                "message": "正在爬取..."
            }
        }
        """
        crawler_state = _crawler_status

        response_data = {
            "has_active_task": crawler_state['running'],
            "mode": crawler_state['mode'],
            "limit": crawler_state['limit'],
            "collected": crawler_state['collected'],
            "message": crawler_state['message'],
            "start_time": crawler_state['start_time']
        }

        return Response(
            make_response(code=0, data=response_data),
            status=status.HTTP_200_OK
        )


class CrawlerStartView(APIView):
    """
    启动爬虫任务 API (使用 Django 管理命令)

    POST /api/crawler/start/

    请求参数:
    {
        "mode": "demo" | "full",  // 采集模式
        "limit": 20               // 采集数量限制
    }

    响应示例:
    {
        "code": 0,
        "data": {
            "message": "爬虫任务已启动"
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request):
        import subprocess
        import threading
        import sys
        import os
        from datetime import datetime
        from pathlib import Path

        try:
            # 权限检查：仅管理员可启动爬虫
            if not hasattr(request.user, 'role') or request.user.role != 'admin':
                return Response(
                    make_response(code=-1, message="仅管理员可以启动爬虫任务"),
                    status=status.HTTP_403_FORBIDDEN
                )

            # 检查是否已有任务在运行
            if _crawler_status['running']:
                return Response(
                    make_response(
                        code=-1,
                        message=f"已有任务正在运行 (模式: {_crawler_status['mode']})",
                    ),
                    status=status.HTTP_409_CONFLICT
                )

            # 获取请求参数
            mode = request.data.get('mode', 'demo')
            try:
                limit = int(request.data.get('limit', 20))
            except (ValueError, TypeError):
                return Response(
                    make_response(code=-1, message="参数 limit 必须是整数"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 参数验证
            if mode not in ['demo', 'full']:
                return Response(
                    make_response(code=-1, message="参数 mode 无效，仅支持 'demo' 或 'full'"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            if limit < 1 or limit > 50000:
                return Response(
                    make_response(code=-1, message="参数 limit 超出范围，应为 1-50000"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 生成输出文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f'crawler_{mode}_{timestamp}.csv'
            output_dir = Path(__file__).parent.parent.parent / 'exports'
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / output_filename

            # 更新状态
            _crawler_status.update({
                'running': True,
                'mode': mode,
                'limit': limit,
                'collected': 0,
                'message': '正在启动...',
                'start_time': datetime.now().isoformat(),
                'output_file': str(output_path)
            })

            # 在后台线程中运行爬虫
            def run_crawler():
                try:
                    backend_dir = Path(__file__).parent.parent.parent

                    # 使用 Django 管理命令运行爬虫
                    cmd = [
                        sys.executable, 'manage.py', 'run_crawler',
                        '--mode', mode,
                        '--limit', str(limit),
                        '--output', str(output_path)
                    ]

                    _crawler_status['message'] = '正在爬取...'

                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=3600,  # 1小时超时
                        cwd=str(backend_dir),
                        env=os.environ.copy()
                    )

                    # 解析结果
                    collected = 0
                    for line in result.stdout.split('\n'):
                        if 'item_scraped_count' in line:
                            try:
                                collected = int(line.split('item_scraped_count')[-1].strip().rstrip(','))
                            except:
                                pass

                    if result.returncode == 0:
                        _crawler_status.update({
                            'running': False,
                            'collected': collected,
                            'message': f'完成! 采集 {collected} 条',
                            'output_file': str(output_path),
                            'csv_ready': True
                        })
                    else:
                        _crawler_status.update({
                            'running': False,
                            'collected': collected,
                            'message': f'失败: {result.stderr[:200] if result.stderr else "未知错误"}'
                        })
                except subprocess.TimeoutExpired:
                    _crawler_status.update({
                        'running': False,
                        'message': '超时: 任务运行超过1小时'
                    })
                except Exception as e:
                    _crawler_status.update({
                        'running': False,
                        'message': f'错误: {str(e)}'
                    })

            # 启动后台线程
            thread = threading.Thread(target=run_crawler, daemon=True)
            thread.start()

            return Response(
                make_response(
                    code=0,
                    data={
                        "mode": mode,
                        "limit": limit,
                        "message": "爬虫任务已启动，请稍后查看状态",
                        "output_file": output_filename
                    },
                    message="爬虫任务已启动"
                ),
                status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"系统繁忙，请稍后重试: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CrawlerStopView(APIView):
    """
    停止爬虫任务 API (简化版)

    POST /api/crawler/stop/

    注意：由于使用 subprocess 执行，实际无法强制终止。
    此接口仅标记状态为已停止。
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request):
        # 权限检查：仅管理员可停止爬虫
        if not hasattr(request.user, 'role') or request.user.role != 'admin':
            return Response(
                make_response(code=-1, message="仅管理员可以停止爬虫任务"),
                status=status.HTTP_403_FORBIDDEN
            )

        # 检查是否有运行中的任务
        if not _crawler_status['running']:
            return Response(
                make_response(code=-1, message="没有正在运行的爬虫任务"),
                status=status.HTTP_404_NOT_FOUND
            )

        # 标记为已停止（注意：实际进程可能仍在运行）
        _crawler_status.update({
            'running': False,
            'message': '已手动停止'
        })

        return Response(
            make_response(
                code=0,
                data={
                    "message": "爬虫任务已停止",
                    "note": "由于使用 subprocess，进程可能仍在后台运行，请手动检查"
                }
            ),
            status=status.HTTP_200_OK
        )


class CrawlerDownloadView(APIView):
    """
    下载爬取的 CSV 文件 API

    GET /api/crawler/download/

    返回最近的爬取结果 CSV 文件
    """
    permission_classes = [permissions.AllowAny]  # 允许任何人下载

    def get(self, request):
        from pathlib import Path
        from django.http import FileResponse
        import mimetypes

        try:
            # 获取输出目录 - 修正路径到 apps/crawler/exports/
            output_dir = Path(__file__).parent.parent.parent / 'apps' / 'crawler' / 'exports'

            # 查找最新的 CSV 文件
            csv_files = list(output_dir.glob('crawler_*.csv'))

            if not csv_files:
                # 如果没有爬取生成的文件，从数据库生成 CSV
                from apps.crawler.models import Question
                import csv
                from io import StringIO
                from django.http import HttpResponse

                # 获取最近采集的数据
                questions = Question.objects.order_by('-created_at')[:1000]

                # 创建 CSV
                output = StringIO()
                writer = csv.writer(output)

                # 写入表头
                writer.writerow([
                    '问题ID', '标题', '分类', '回答数', '发布时间',
                    '地理位置', '来源链接', '采集时间', '采集页码'
                ])

                # 写入数据
                for q in questions:
                    writer.writerow([
                        q.question_id,
                        q.title,
                        q.category or '',
                        q.answer_count,
                        q.publish_time.strftime('%Y-%m-%d') if q.publish_time else '',
                        q.location or '',
                        q.source_url,
                        q.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        q.crawl_page
                    ])

                # 创建响应
                response = HttpResponse(
                    output.getvalue(),
                    content_type='text/csv; charset=utf-8-sig'
                )
                response['Content-Disposition'] = f'attachment; filename="questions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
                return response

            # 获取最新文件
            latest_file = max(csv_files, key=lambda p: p.stat().st_mtime)

            # 返回文件
            response = FileResponse(
                open(latest_file, 'rb'),
                content_type='text/csv'
            )
            response['Content-Disposition'] = f'attachment; filename="{latest_file.name}"'
            return response

        except Exception as e:
            return Response(
                make_response(code=-1, message=f"下载失败: {str(e)}"),
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
                make_response(code=-1, message="系统繁忙，请稍后重试"),
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
                make_response(code=-1, message="系统繁忙，请稍后重试"),
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
                make_response(code=-1, message="系统繁忙，请稍后重试"),
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
                make_response(code=-1, message="系统繁忙，请稍后重试"),
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
    queryset = Question.objects.prefetch_related('answers').all()
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
        - category: 分类筛选
        - location: 地理位置筛选
        - publish_time_after: 发布时间起始（格式：YYYY-MM-DD）
        - publish_time_before: 发布时间结束（格式：YYYY-MM-DD）
        - answer_count_min: 回答数量最小值
        - answer_count_max: 回答数量最大值
        """
        # 获取查询参数
        search = request.query_params.get('search', '')
        ordering = request.query_params.get('ordering', '-created_at')

        # 构建查询集
        queryset = self.get_queryset()

        if search:
            queryset = queryset.filter(title__icontains=search)

        # 分类筛选
        category = request.query_params.get('category', '')
        if category:
            queryset = queryset.filter(category=category)

        # 地理位置筛选
        location = request.query_params.get('location', '')
        if location:
            queryset = queryset.filter(location=location)

        # 发布时间范围筛选
        publish_time_after = request.query_params.get('publish_time_after')
        publish_time_before = request.query_params.get('publish_time_before')
        if publish_time_after:
            queryset = queryset.filter(publish_time__gte=publish_time_after)
        if publish_time_before:
            queryset = queryset.filter(publish_time__lte=publish_time_before)

        # 回答数量范围筛选
        answer_count_min = request.query_params.get('answer_count_min')
        answer_count_max = request.query_params.get('answer_count_max')
        if answer_count_min:
            queryset = queryset.filter(answer_count__gte=int(answer_count_min))
        if answer_count_max:
            queryset = queryset.filter(answer_count__lte=int(answer_count_max))

        # 排序（添加 answer_count 排序选项）
        valid_orderings = ['created_at', '-created_at', 'publish_time', '-publish_time', 'answer_count', '-answer_count']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')

        # 分页
        try:
            page = int(request.query_params.get('page', 1))
            if page < 1:
                return Response(
                    make_response(code=-1, message="参数 page 必须是大于 0 的整数"),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                make_response(code=-1, message="参数 page 必须是整数"),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            page_size = int(request.query_params.get('page_size', 20))
            if page_size < 1:
                return Response(
                    make_response(code=-1, message="参数 page_size 必须是大于 0 的整数"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            page_size = min(page_size, 100)
        except (ValueError, TypeError):
            return Response(
                make_response(code=-1, message="参数 page_size 必须是整数"),
                status=status.HTTP_400_BAD_REQUEST
            )

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

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        """
        获取问答完整详情（包含所有字段）

        GET /api/questions/<id>/detail/
        """
        question = get_object_or_404(Question.objects.prefetch_related('answers'), pk=pk)
        serializer = self.get_serializer(question)
        return Response(
            make_response(code=0, data=serializer.data),
            status=status.HTTP_200_OK
        )


class StatisticsTrendView(APIView):
    """
    统计分析 API - 每日问答数量趋势

    GET /api/statistics/trend/

    返回格式（与 ECharts 兼容）：
    {
        "code": 0,
        "data": [
            {"date": "2026-02-01", "count": 120},
            {"date": "2026-02-02", "count": 150},
            ...
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取每日问答数量趋势

        可选参数：
        - days: 返回最近天数（默认30，最大365）
        """
        try:
            days = int(request.query_params.get('days', 30))
            if days < 1:
                return Response(
                    make_response(code=-1, message="参数 days 必须是大于 0 的整数"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            if days > 365:
                return Response(
                    make_response(code=-1, message="参数 days 不能超过 365"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            days = min(days, 365)
        except (ValueError, TypeError):
            return Response(
                make_response(code=-1, message="参数 days 必须是整数"),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 按日期分组统计问答数量
            # 优先使用 publish_time（问题的发布时间），如果没有则使用 created_at（入库时间）
            from django.db.models import Count
            from collections import defaultdict

            # 使用 publish_time 进行统计
            trend_dict = defaultdict(int)

            # 获取所有有 publish_time 的记录
            questions_with_date = Question.objects.filter(
                publish_time__isnull=False
            ).values_list('publish_time', flat=True)

            for date in questions_with_date:
                # publish_time 是 DateField，直接使用
                date_str = date.strftime('%Y-%m-%d')
                trend_dict[date_str] += 1

            # 转换为排序列表
            trend_list = [
                {"date": date, "count": count}
                for date, count in sorted(trend_dict.items())
            ]

            return Response(
                make_response(code=0, data=trend_list),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatisticsCategoriesView(APIView):
    """
    统计分析 API - 分类统计

    GET /api/statistics/categories/

    返回格式（与 ECharts 词云图兼容）：
    {
        "code": 0,
        "data": [
            {"name": "影视", "value": 150},
            {"name": "烦恼", "value": 120},
            ...
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取分类统计（前50）

        可选参数：
        - limit: 返回数量（默认50，最大100）
        """
        try:
            limit = int(request.query_params.get('limit', 50))
            if limit < 1:
                return Response(
                    make_response(code=-1, message="参数 limit 必须是大于 0 的整数"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            if limit > 100:
                return Response(
                    make_response(code=-1, message="参数 limit 不能超过 100"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            limit = min(limit, 100)
        except (ValueError, TypeError):
            return Response(
                make_response(code=-1, message="参数 limit 必须是整数"),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 统计每个分类的问题数量
            category_stats = (
                Question.objects
                .filter(category__isnull=False)
                .exclude(category='')
                .values('category')
                .annotate(question_count=Count('id'))
                .order_by('-question_count')[:limit]
            )

            # 转换为 ECharts 词云格式
            category_list = [
                {
                    "name": item['category'],
                    "value": item['question_count']
                }
                for item in category_stats
            ]

            return Response(
                make_response(code=0, data=category_list),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatisticsAnswerersView(APIView):
    """
    统计分析 API - 高频回答者排名

    GET /api/statistics/answerers/

    返回格式（与 ECharts 柱状图兼容）：
    {
        "code": 0,
        "data": [
            {"name": "user123", "count": 50},
            {"name": "expert456", "count": 35},
            ...
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取高频回答者排名（前20）

        可选参数：
        - limit: 返回数量（默认20，最大50）
        """
        try:
            limit = int(request.query_params.get('limit', 20))
            if limit < 1:
                return Response(
                    make_response(code=-1, message="参数 limit 必须是大于 0 的整数"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            if limit > 50:
                return Response(
                    make_response(code=-1, message="参数 limit 不能超过 50"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            limit = min(limit, 50)
        except (ValueError, TypeError):
            return Response(
                make_response(code=-1, message="参数 limit 必须是整数"),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 统计每个回答者的回答数量（从Answer模型统计）
            answerer_stats = (
                Answer.objects
                .filter(answerer__isnull=False)
                .exclude(answerer='')
                .values('answerer')
                .annotate(count=Count('id'))
                .order_by('-count')[:limit]
            )

            # 转换为列表格式
            answerer_list = [
                {
                    "name": item['answerer'],
                    "count": item['count']
                }
                for item in answerer_stats
            ]

            return Response(
                make_response(code=0, data=answerer_list),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatisticsOverviewView(APIView):
    """
    统计分析 API - 数据总览

    GET /api/statistics/overview/

    返回格式：
    {
        "code": 0,
        "data": {
            "total_questions": 10000,
            "total_categories": 200,
            "total_answerers": 500,
            "total_answers": 15000,
            "today_questions": 150,
            "avg_daily": 100
        }
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取数据总览统计
        """
        try:
            from django.utils import timezone
            from datetime import timedelta

            today = timezone.now().date()
            today_start = timezone.make_aware(
                timezone.datetime.combine(today, timezone.datetime.min.time())
            )

            # 总问答数
            total_questions = Question.objects.count()

            # 总分类数（统计不同的category值）
            total_categories = (
                Question.objects
                .filter(category__isnull=False)
                .exclude(category='')
                .values('category')
                .distinct()
                .count()
            )

            # 总回答数
            total_answers = Answer.objects.count()

            # 总回答者数量（从Answer模型统计）
            total_answerers = (
                Answer.objects
                .filter(answerer__isnull=False)
                .exclude(answerer='')
                .values('answerer')
                .distinct()
                .count()
            )

            # 今日问答数
            today_questions = Question.objects.filter(created_at__gte=today_start).count()

            # 日均问答数（最近30天）
            thirty_days_ago = today_start - timedelta(days=30)
            recent_questions = Question.objects.filter(created_at__gte=thirty_days_ago).count()
            avg_daily = round(recent_questions / 30, 1)

            overview = {
                "total_questions": total_questions,
                "total_categories": total_categories,
                "total_answerers": total_answerers,
                "total_answers": total_answers,
                "today_questions": today_questions,
                "avg_daily": avg_daily
            }

            return Response(
                make_response(code=0, data=overview),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuestionFilterOptionsView(APIView):
    """获取问答筛选选项"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取可选的分类和位置列表"""
        # 获取所有不同的分类
        categories = Question.objects.filter(
            category__isnull=False
        ).exclude(category='').values_list('category', flat=True).distinct()

        # 获取所有不同的位置
        locations = Question.objects.filter(
            location__isnull=False
        ).exclude(location='').values_list('location', flat=True).distinct()

        return Response(
            make_response(code=0, data={
                'categories': list(categories),
                'locations': list(locations)
            })
        )


class StatisticsLocationView(APIView):
    """
    统计分析 API - 地理位置分布

    GET /api/statistics/locations/

    返回格式:
    {
        "code": 0,
        "data": [
            {"name": "广东", "value": 150},
            {"name": "北京", "value": 120},
            ...
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 20))
            limit = min(limit, 50)
        except (ValueError, TypeError):
            limit = 20

        try:
            location_data = (
                Question.objects
                .exclude(location__isnull=True)
                .exclude(location='')
                .values('location')
                .annotate(value=Count('id'))
                .order_by('-value')[:limit]
            )

            data = [
                {"name": item['location'], "value": item['value']}
                for item in location_data
            ]

            return Response(make_response(code=0, data=data))
        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatisticsHotQuestionsView(APIView):
    """
    统计分析 API - 热门问题

    GET /api/statistics/hot-questions/

    返回格式:
    {
        "code": 0,
        "data": [
            {"title": "问题标题", "answer_count": 25, "category": "影视"},
            ...
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 10))
            limit = min(limit, 20)
        except (ValueError, TypeError):
            limit = 10

        try:
            hot_questions = (
                Question.objects
                .filter(answer_count__gt=0)
                .values('title', 'answer_count', 'category')
                .order_by('-answer_count')[:limit]
            )

            data = [
                {
                    "title": item['title'][:50] + '...' if len(item['title']) > 50 else item['title'],
                    "answer_count": item['answer_count'],
                    "category": item['category'] or '未分类'
                }
                for item in hot_questions
            ]

            return Response(make_response(code=0, data=data))
        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StatisticsAnswerDistributionView(APIView):
    """
    统计分析 API - 回答数量分布

    GET /api/statistics/answer-distribution/

    返回格式:
    {
        "code": 0,
        "data": [
            {"range": "0", "count": 150, "label": "无回答"},
            {"range": "1-3", "count": 80, "label": "1-3个"},
            {"range": "4-10", "count": 45, "label": "4-10个"},
            {"range": "10+", "count": 25, "label": "10个以上"}
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # 统计各回答数区间的数量
            zero = Question.objects.filter(answer_count=0).count()
            one_three = Question.objects.filter(answer_count__gte=1, answer_count__lte=3).count()
            four_ten = Question.objects.filter(answer_count__gte=4, answer_count__lte=10).count()
            over_ten = Question.objects.filter(answer_count__gt=10).count()

            data = [
                {"range": "0", "count": zero, "label": "无回答"},
                {"range": "1-3", "count": one_three, "label": "1-3个"},
                {"range": "4-10", "count": four_ten, "label": "4-10个"},
                {"range": "10+", "count": over_ten, "label": "10个以上"}
            ]

            return Response(make_response(code=0, data=data))
        except Exception as e:
            return Response(
                make_response(code=-1, message="系统繁忙，请稍后重试"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
