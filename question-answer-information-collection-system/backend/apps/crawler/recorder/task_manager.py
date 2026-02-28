"""
任务状态管理器 - 负责爬虫任务状态的创建、保存和管理
"""
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List


class TaskStatus:
    """任务状态常量"""
    PENDING = 'pending'
    RUNNING = 'running'
    PAUSED = 'paused'
    COMPLETED = 'completed'
    FAILED = 'failed'

    VALID_STATUSES = {PENDING, RUNNING, PAUSED, COMPLETED, FAILED}


class TaskManager:
    """任务状态管理器"""

    def __init__(self, status_dir: str = None):
        """初始化任务管理器

        Args:
            status_dir: 任务状态文件存储目录，默认为 recorder/statuses
        """
        if status_dir is None:
            base_dir = Path(__file__).parent
            status_dir = base_dir / 'statuses'
        self.status_dir = Path(status_dir)
        self.status_dir.mkdir(parents=True, exist_ok=True)

    def _get_status_file(self, task_id: str) -> Path:
        """获取任务状态文件路径"""
        return self.status_dir / f'{task_id}.json'

    def _validate_task_id(self, task_id: str) -> str:
        """验证任务ID格式"""
        if not task_id or not isinstance(task_id, str):
            raise ValueError("Invalid task_id: must be a non-empty string")
        # UUID 格式验证
        try:
            uuid.UUID(task_id)
        except (ValueError, AttributeError):
            raise ValueError("Invalid task_id: must be a valid UUID")
        return task_id

    def _validate_filename(self, filename: str) -> str:
        """验证文件名，防止路径遍历攻击"""
        if '..' in filename or os.sep in filename or '/' in filename or '\\' in filename:
            raise ValueError("Invalid filename: path traversal not allowed")
        # 禁止特殊字符
        if any(c in filename for c in ['<', '>', ':', '"', '|', '?', '*']):
            raise ValueError("Invalid filename: special characters not allowed")
        return filename

    def _load_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """加载任务状态"""
        task_id = self._validate_task_id(task_id)
        filepath = self._get_status_file(task_id)
        if not filepath.exists():
            return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load task status: {e}")

    def _save_task_status(self, task_id: str, status: Dict[str, Any]) -> None:
        """保存任务状态"""
        task_id = self._validate_task_id(task_id)
        filepath = self._get_status_file(task_id)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save task status: {e}")

    def create_task(self, config_file: str, name: str) -> str:
        """创建新任务

        Args:
            config_file: 配置文件名
            name: 任务名称

        Returns:
            task_id: 新创建的任务ID
        """
        # 验证配置文件名
        config_file = self._validate_filename(config_file)

        # 生成任务ID
        task_id = str(uuid.uuid4())

        # 创建任务状态
        status = {
            'task_id': task_id,
            'name': name,
            'config_file': config_file,
            'status': TaskStatus.PENDING,
            'progress': {
                'current_page': 1,
                'total_pages': 500,
                'items_collected': 0,
                'failed_items': 0
            },
            'timing': {
                'started_at': None,
                'paused_at': None,
                'resumed_at': None,
                'completed_at': None,
                'total_runtime_seconds': 0
            },
            'interval_config': {
                'initial': 2,
                'increment': 1,
                'max': 10,
                'current': 2
            },
            'error_log': [],
            'last_item_index': 0,
            'last_detail_url': None,
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z'
        }

        self._save_task_status(task_id, status)
        return task_id

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态字典，如果任务不存在返回None
        """
        return self._load_task_status(task_id)

    def save_task_status(self, task_id: str, status: str) -> bool:
        """保存任务状态

        Args:
            task_id: 任务ID
            status: 任务状态值

        Returns:
            是否保存成功
        """
        # 验证状态值
        if status not in TaskStatus.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {TaskStatus.VALID_STATUSES}")

        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        task_status['status'] = status
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def update_progress(self, task_id: str, **kwargs) -> bool:
        """更新进度

        Args:
            task_id: 任务ID
            **kwargs: 可更新的进度字段，如 current_page, total_pages, items_collected, failed_items

        Returns:
            是否更新成功
        """
        allowed_fields = {'current_page', 'total_pages', 'items_collected', 'failed_items',
                          'last_item_index', 'last_detail_url'}

        invalid_fields = set(kwargs.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Invalid progress fields: {invalid_fields}")

        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        for key, value in kwargs.items():
            if key in ['current_page', 'total_pages', 'items_collected', 'failed_items', 'last_item_index']:
                if not isinstance(value, int) or value < 0:
                    raise ValueError(f"Invalid value for {key}: must be a non-negative integer")
            task_status['progress'][key] = value
            task_status[key] = value

        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def update_timing(self, task_id: str, **kwargs) -> bool:
        """更新时间信息

        Args:
            task_id: 任务ID
            **kwargs: 可更新的时间字段

        Returns:
            是否更新成功
        """
        allowed_fields = {'started_at', 'paused_at', 'resumed_at', 'completed_at', 'total_runtime_seconds'}

        invalid_fields = set(kwargs.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Invalid timing fields: {invalid_fields}")

        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        for key, value in kwargs.items():
            if key == 'total_runtime_seconds':
                if not isinstance(value, (int, float)) or value < 0:
                    raise ValueError("total_runtime_seconds must be a non-negative number")
            task_status['timing'][key] = value

        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def add_error(self, task_id: str, error: str) -> bool:
        """添加错误日志

        Args:
            task_id: 任务ID
            error: 错误信息

        Returns:
            是否添加成功
        """
        if not error or not isinstance(error, str):
            raise ValueError("Invalid error: must be a non-empty string")

        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        error_entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'error': error
        }
        task_status['error_log'].append(error_entry)
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def start_task(self, task_id: str) -> bool:
        """开始任务

        Args:
            task_id: 任务ID

        Returns:
            是否操作成功
        """
        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        # 只有 pending, paused 或 failed 状态的任务才能启动
        if task_status['status'] not in [TaskStatus.PENDING, TaskStatus.PAUSED, TaskStatus.FAILED]:
            raise ValueError(f"Cannot start task in '{task_status['status']}' status")

        task_status['status'] = TaskStatus.RUNNING
        task_status['timing']['started_at'] = datetime.now().isoformat() + 'Z'
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def pause_task(self, task_id: str) -> bool:
        """暂停任务

        Args:
            task_id: 任务ID

        Returns:
            是否操作成功
        """
        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        if task_status['status'] != TaskStatus.RUNNING:
            raise ValueError(f"Cannot pause task in '{task_status['status']}' status")

        task_status['status'] = TaskStatus.PAUSED
        task_status['timing']['paused_at'] = datetime.now().isoformat() + 'Z'
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def resume_task(self, task_id: str) -> bool:
        """继续任务

        Args:
            task_id: 任务ID

        Returns:
            是否操作成功
        """
        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        if task_status['status'] != TaskStatus.PAUSED:
            raise ValueError(f"Cannot resume task in '{task_status['status']}' status")

        task_status['status'] = TaskStatus.RUNNING
        task_status['timing']['resumed_at'] = datetime.now().isoformat() + 'Z'
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def complete_task(self, task_id: str) -> bool:
        """完成任务

        Args:
            task_id: 任务ID

        Returns:
            是否操作成功
        """
        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        task_status['status'] = TaskStatus.COMPLETED
        task_status['timing']['completed_at'] = datetime.now().isoformat() + 'Z'
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def fail_task(self, task_id: str, error_message: str) -> bool:
        """任务失败

        Args:
            task_id: 任务ID
            error_message: 错误信息

        Returns:
            是否操作成功
        """
        if not error_message or not isinstance(error_message, str):
            raise ValueError("Invalid error_message: must be a non-empty string")

        task_status = self._load_task_status(task_id)
        if task_status is None:
            return False

        task_status['status'] = TaskStatus.FAILED
        task_status['timing']['completed_at'] = datetime.now().isoformat() + 'Z'

        # 添加失败原因到错误日志
        error_entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'error': error_message,
            'type': 'fatal'
        }
        task_status['error_log'].append(error_entry)
        task_status['updated_at'] = datetime.now().isoformat() + 'Z'
        self._save_task_status(task_id, task_status)
        return True

    def list_tasks(self) -> List[Dict[str, Any]]:
        """列出所有任务

        Returns:
            任务列表
        """
        tasks = []
        for f in self.status_dir.glob('*.json'):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    task = json.load(file)
                    # 只返回关键字段
                    tasks.append({
                        'task_id': task.get('task_id'),
                        'name': task.get('name'),
                        'config_file': task.get('config_file'),
                        'status': task.get('status'),
                        'progress': task.get('progress'),
                        'created_at': task.get('created_at'),
                        'updated_at': task.get('updated_at')
                    })
            except (IOError, json.JSONDecodeError):
                continue
        return sorted(tasks, key=lambda x: x.get('updated_at', ''), reverse=True)

    def delete_task(self, task_id: str) -> bool:
        """删除任务

        Args:
            task_id: 任务ID

        Returns:
            是否删除成功
        """
        task_id = self._validate_task_id(task_id)
        filepath = self._get_status_file(task_id)
        try:
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except OSError as e:
            raise IOError(f"Failed to delete task: {e}")
