"""
录制爬虫 API 视图
"""
import asyncio
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from .recorder import Recorder
from .config_manager import ConfigManager
from .task_manager import TaskManager

# 配置日志
logger = logging.getLogger(__name__)

# 全局实例
_recorder = Recorder(headless=False)
_config_manager = ConfigManager()
_task_manager = TaskManager()


def _run_async(coro):
    """运行异步函数的辅助函数"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _parse_json_body(request):
    """解析请求体中的 JSON 数据"""
    try:
        return json.loads(request.body.decode('utf-8')) if request.body else {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")


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


# ==================== 录制相关 API ====================

@csrf_exempt
@require_http_methods(["POST"])
def start_recording(request):
    """启动录制"""
    try:
        body = _parse_json_body(request)
        url = body.get('url')

        # 检查是否已经在录制
        if _recorder.is_recording():
            return JsonResponse(make_response(
                code=-1,
                message="录制器已在运行中"
            ))

        # 启动录制
        _run_async(_recorder.start(url=url))

        return JsonResponse(make_response(
            data={
                "recording": True,
                "current_url": _recorder.current_url
            },
            message="录制已启动"
        ))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"启动录制失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"启动录制失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def stop_recording(request):
    """停止录制"""
    try:
        if not _recorder.is_recording():
            return JsonResponse(make_response(
                code=-1,
                message="录制器未在运行"
            ))

        # 停止录制并获取步骤
        steps = _run_async(_recorder.stop())

        return JsonResponse(make_response(
            data={
                "recording": False,
                "steps_count": len(steps),
                "steps": steps
            },
            message="录制已停止"
        ))
    except Exception as e:
        logger.error(f"停止录制失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"停止录制失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["GET"])
def get_recording_steps(request):
    """获取录制步骤"""
    try:
        # 同步步骤
        _run_async(_recorder.sync_steps())
        steps = _run_async(_recorder.get_steps())

        return JsonResponse(make_response(
            data={
                "steps_count": len(steps),
                "steps": steps
            }
        ))
    except Exception as e:
        logger.error(f"获取录制步骤失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"获取录制步骤失败: {str(e)}"))


# ==================== 配置相关 API ====================

@csrf_exempt
@require_http_methods(["GET"])
def list_configs(request):
    """列出所有配置"""
    try:
        configs = _config_manager.list_configs()
        return JsonResponse(make_response(
            data=configs,
            total=len(configs)
        ))
    except Exception as e:
        logger.error(f"列出配置失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"列出配置失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["GET"])
def get_config(request):
    """获取配置详情"""
    try:
        filename = request.GET.get('filename')
        if not filename:
            return JsonResponse(make_response(code=-1, message="缺少 filename 参数"))

        config = _config_manager.load_config(filename)
        if config is None:
            return JsonResponse(make_response(code=-1, message="配置文件不存在"))

        return JsonResponse(make_response(data=config))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"获取配置失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def create_config(request):
    """创建新配置"""
    try:
        body = _parse_json_body(request)
        name = body.get('name', '未命名配置')

        config = _config_manager.create_config(name)
        filepath = _config_manager.save_config(config)

        return JsonResponse(make_response(
            data={
                "filename": filepath,
                "config": config
            },
            message="配置已创建"
        ))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"创建配置失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"创建配置失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def save_config(request):
    """保存配置"""
    try:
        body = _parse_json_body(request)
        filename = body.get('filename')
        config = body.get('config')

        if not filename or not config:
            return JsonResponse(make_response(code=-1, message="缺少 filename 或 config 参数"))

        filepath = _config_manager.save_config(config, filename)

        return JsonResponse(make_response(
            data={"filepath": filepath},
            message="配置已保存"
        ))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"保存配置失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"保存配置失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def delete_config(request):
    """删除配置"""
    try:
        body = _parse_json_body(request)
        filename = body.get('filename')
        if not filename:
            return JsonResponse(make_response(code=-1, message="缺少 filename 参数"))

        success = _config_manager.delete_config(filename)
        if not success:
            return JsonResponse(make_response(code=-1, message="配置文件不存在"))

        return JsonResponse(make_response(message="配置已删除"))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"删除配置失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"删除配置失败: {str(e)}"))


# ==================== 任务相关 API ====================

@csrf_exempt
@require_http_methods(["GET"])
def list_tasks(request):
    """列出所有任务"""
    try:
        tasks = _task_manager.list_tasks()
        return JsonResponse(make_response(
            data=tasks,
            total=len(tasks)
        ))
    except Exception as e:
        logger.error(f"列出任务失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"列出任务失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def create_task(request):
    """创建新任务"""
    try:
        body = _parse_json_body(request)
        config_file = body.get('config_file')
        name = body.get('name', '未命名任务')

        if not config_file:
            return JsonResponse(make_response(code=-1, message="缺少 config_file 参数"))

        task_id = _task_manager.create_task(config_file, name)

        return JsonResponse(make_response(
            data={"task_id": task_id},
            message="任务已创建"
        ))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"创建任务失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"创建任务失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["GET"])
def get_task_status(request, task_id):
    """获取任务状态"""
    try:
        task_status = _task_manager.get_task_status(task_id)
        if task_status is None:
            return JsonResponse(make_response(code=-1, message="任务不存在"))

        return JsonResponse(make_response(data=task_status))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"获取任务状态失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def start_task(request, task_id):
    """开始任务"""
    try:
        success = _task_manager.start_task(task_id)
        if not success:
            return JsonResponse(make_response(code=-1, message="任务不存在"))

        return JsonResponse(make_response(message="任务已开始"))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"开始任务失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"开始任务失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def pause_task(request, task_id):
    """暂停任务"""
    try:
        success = _task_manager.pause_task(task_id)
        if not success:
            return JsonResponse(make_response(code=-1, message="任务不存在"))

        return JsonResponse(make_response(message="任务已暂停"))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"暂停任务失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"暂停任务失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def resume_task(request, task_id):
    """继续任务"""
    try:
        success = _task_manager.resume_task(task_id)
        if not success:
            return JsonResponse(make_response(code=-1, message="任务不存在"))

        return JsonResponse(make_response(message="任务已继续"))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"继续任务失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"继续任务失败: {str(e)}"))


@csrf_exempt
@require_http_methods(["POST"])
def stop_task(request, task_id):
    """停止任务"""
    try:
        # 使用 fail_task 来标记任务停止
        body = _parse_json_body(request)
        reason = body.get('reason', '用户手动停止')

        success = _task_manager.fail_task(task_id, reason)
        if not success:
            return JsonResponse(make_response(code=-1, message="任务不存在"))

        return JsonResponse(make_response(message="任务已停止"))
    except ValueError as e:
        return JsonResponse(make_response(code=-1, message=str(e)))
    except Exception as e:
        logger.error(f"停止任务失败: {e}")
        return JsonResponse(make_response(code=-1, message=f"停止任务失败: {str(e)}"))
