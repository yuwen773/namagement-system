"""
配置编辑器 - 负责手动编辑和调整录制配置的功能
"""
from typing import Dict, Any, Optional, List


class ConfigEditor:
    """配置编辑器 - 用于手动编辑和调整录制配置"""

    def __init__(self, config_manager):
        """
        初始化配置编辑器

        Args:
            config_manager: ConfigManager 实例
        """
        self.config_manager = config_manager

    def load_config(self, filename: str) -> Optional[Dict]:
        """
        加载配置

        Args:
            filename: 配置文件名

        Returns:
            配置字典，如果文件不存在则返回 None
        """
        return self.config_manager.load_config(filename)

    def save_config(self, config: Dict, filename: str) -> str:
        """
        保存配置

        Args:
            config: 配置字典
            filename: 配置文件名

        Returns:
            保存的文件路径
        """
        return self.config_manager.save_config(config, filename)

    def add_list_config(
        self,
        config: Dict,
        item_selector: str,
        fields: List[Dict],
        pagination_selector: str = '',
        max_pages: int = 500
    ) -> Dict:
        """
        添加列表提取配置

        Args:
            config: 配置字典
            item_selector: 列表项选择器
            fields: 字段配置列表
            pagination_selector: 翻页选择器
            max_pages: 最大翻页数

        Returns:
            更新后的配置字典
        """
        config['list_config'] = {
            'item_selector': item_selector,
            'fields': fields,
            'pagination': {
                'type': 'click',
                'selector': pagination_selector,
                'max_pages': max_pages
            }
        }
        return config

    def add_detail_config(
        self,
        config: Dict,
        entry_selector: str,
        fields: List[Dict]
    ) -> Dict:
        """
        添加详情页配置

        Args:
            config: 配置字典
            entry_selector: 详情页入口选择器
            fields: 字段配置列表

        Returns:
            更新后的配置字典
        """
        config['detail_config'] = {
            'entry': {
                'type': 'click',
                'selector': entry_selector
            },
            'fields': fields
        }
        return config

    def add_field(
        self,
        config: Dict,
        field_config: Dict,
        is_list: bool = False,
        parent_selector: str = ''
    ) -> Dict:
        """
        添加字段配置

        Args:
            config: 配置字典
            field_config: 字段配置 {
                'name': '字段名',
                'selector': 'CSS选择器',
                'type': 'text|attribute|html',
                'attribute': '属性名'  # 当type为attribute时需要
            }
            is_list: 是否为列表字段
            parent_selector: 父级选择器

        Returns:
            更新后的配置字典
        """
        field = {
            'name': field_config.get('name', ''),
            'selector': field_config.get('selector', ''),
            'type': field_config.get('type', 'text'),
        }

        if field_config.get('attribute'):
            field['attribute'] = field_config['attribute']

        if is_list:
            field['is_list'] = True

        if parent_selector:
            field['parent_selector'] = parent_selector

        # 确定添加到哪个配置中
        if 'detail_config' in field_config.get('target', ''):
            # 添加到详情页配置
            if 'detail_config' not in config:
                config['detail_config'] = {'entry': {'selector': ''}, 'fields': []}
            config['detail_config']['fields'].append(field)
        else:
            # 添加到列表配置
            if 'list_config' not in config:
                config['list_config'] = {'item_selector': '', 'pagination': {}, 'fields': []}
            config['list_config']['fields'].append(field)

        return config

    def validate_config(self, config: Dict) -> List[str]:
        """
        验证配置

        Args:
            config: 配置字典

        Returns:
           信息列表，如果为空 错误则表示验证通过
        """
        errors = []

        # 检查必要字段
        if not config.get('name'):
            errors.append('name 不能为空')

        # 检查 list_config
        list_config = config.get('list_config', {})
        if not list_config.get('item_selector'):
            errors.append('list_config.item_selector 不能为空')

        # 检查 detail_config
        detail_config = config.get('detail_config', {})
        entry = detail_config.get('entry', {})
        if not entry.get('selector'):
            errors.append('detail_config.entry.selector 不能为空')

        # 验证字段配置
        list_fields = list_config.get('fields', [])
        if not list_fields:
            errors.append('list_config.fields 不能为空')

        for i, field in enumerate(list_fields):
            if not field.get('name'):
                errors.append(f'list_config.fields[{i}].name 不能为空')
            if not field.get('selector'):
                errors.append(f'list_config.fields[{i}].selector 不能为空')

        detail_fields = detail_config.get('fields', [])
        for i, field in enumerate(detail_fields):
            if not field.get('name'):
                errors.append(f'detail_config.fields[{i}].name 不能为空')
            if not field.get('selector'):
                errors.append(f'detail_config.fields[{i}].selector 不能为空')

        return errors

    def generate_default_config(self, name: str) -> Dict:
        """
        生成默认配置模板（360问答）

        Args:
            name: 配置名称

        Returns:
            默认配置字典
        """
        from datetime import datetime

        config = {
            'version': '1.0',
            'name': name,
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z',
            'list_config': {
                'item_selector': 'ul.question-list li',
                'pagination': {
                    'type': 'click',
                    'selector': '.next',
                    'max_pages': 500
                },
                'fields': [
                    {
                        'name': 'title',
                        'selector': '.question-title a',
                        'type': 'text'
                    },
                    {
                        'name': 'url',
                        'selector': '.question-title a',
                        'type': 'attribute',
                        'attribute': 'href'
                    },
                    {
                        'name': 'answer_count',
                        'selector': '.answer-count',
                        'type': 'text'
                    }
                ]
            },
            'detail_config': {
                'entry': {
                    'type': 'click',
                    'selector': '.question-title a'
                },
                'fields': [
                    {
                        'name': 'title',
                        'selector': '.question-title',
                        'type': 'text'
                    },
                    {
                        'name': 'content',
                        'selector': '.question-content',
                        'type': 'text'
                    },
                    {
                        'name': 'answer',
                        'selector': '.answer-content',
                        'type': 'text'
                    },
                    {
                        'name': 'answer_author',
                        'selector': '.answer-author',
                        'type': 'text'
                    },
                    {
                        'name': 'answer_time',
                        'selector': '.answer-time',
                        'type': 'text'
                    }
                ]
            },
            'steps': []
        }

        return config
