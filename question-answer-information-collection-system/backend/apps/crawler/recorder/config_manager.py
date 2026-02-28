"""
配置文件管理器 - 负责录制配置的创建、保存和加载
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置文件管理器"""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            base_dir = Path(__file__).parent
            config_dir = base_dir / 'configs'
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def create_config(self, name: str) -> Dict[str, Any]:
        """创建新的录制配置"""
        config = {
            'version': '1.0',
            'name': name,
            'created_at': datetime.now().isoformat() + 'Z',
            'steps': [],
            'list_config': {
                'item_selector': '',
                'pagination': {
                    'type': 'click',
                    'selector': '',
                    'max_pages': 500
                }
            },
            'detail_config': {
                'entry': {
                    'type': 'click',
                    'selector': ''
                },
                'fields': []
            }
        }
        return config

    def _validate_filename(self, filename: str) -> str:
        """验证文件名，防止路径遍历攻击"""
        # 禁止包含路径分隔符和 ..
        if '..' in filename or os.sep in filename or '/' in filename or '\\' in filename:
            raise ValueError("Invalid filename: path traversal not allowed")
        return filename

    def save_config(self, config: Dict[str, Any], filename: str = None) -> str:
        """保存配置到文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'config_{timestamp}.json'
        else:
            filename = self._validate_filename(filename)

        filepath = self.config_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save config: {e}")

        return str(filepath)

    def load_config(self, filename: str) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        filename = self._validate_filename(filename)
        filepath = self.config_dir / filename
        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load config: {e}")

    def list_configs(self) -> list:
        """列出所有配置文件"""
        configs = []
        for f in self.config_dir.glob('config_*.json'):
            configs.append({
                'filename': f.name,
                'created_at': f.stat().st_mtime
            })
        return sorted(configs, key=lambda x: x['created_at'], reverse=True)

    def delete_config(self, filename: str) -> bool:
        """删除配置文件"""
        filename = self._validate_filename(filename)
        filepath = self.config_dir / filename
        try:
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except OSError as e:
            raise IOError(f"Failed to delete config: {e}")
