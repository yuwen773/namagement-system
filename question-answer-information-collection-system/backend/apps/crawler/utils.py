"""
数据清洗工具模块

提供数据清洗功能，包括 HTML 标签移除、文本规范化、去重和验证。
集成到 Scrapy Pipeline 中使用。
"""

import re
from html import unescape
from typing import Optional, Dict, Any, List


class DataCleaner:
    """
    数据清洗工具类

    用于清洗爬取的原始数据，确保入库数据质量。
    """

    # HTML 标签正则
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')

    # 特殊字符映射（HTML 实体转义）
    HTML_ENTITIES = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&apos;': "'",
        '&cent;': '¢',
        '&pound;': '£',
        '&yen;': '¥',
        '&euro;': '€',
        '&copy;': '©',
        '&reg;': '®',
    }

    # 必填字段
    REQUIRED_FIELDS = ['title', 'answer_content', 'source_url']

    # 字段最大长度限制
    MAX_LENGTHS = {
        'title': 255,
        'answerer': 100,
        'source_url': 255,
    }

    def __init__(self):
        """初始化 DataCleaner"""
        pass

    def clean_html(self, text: Optional[str]) -> str:
        """
        移除 HTML 标签

        Args:
            text: 原始文本，可能包含 HTML 标签

        Returns:
            清理后的纯文本
        """
        if not text:
            return ''

        # 先进行 HTML 实体转义
        text = unescape(text)

        # 移除 HTML 标签
        text = self.HTML_TAG_PATTERN.sub('', text)

        return text.strip()

    def normalize_text(self, text: Optional[str]) -> str:
        """
        文本规范化

        处理特殊字符、多余空格、换行等。

        Args:
            text: 原始文本

        Returns:
            规范化后的文本
        """
        if not text:
            return ''

        # 替换 HTML 实体
        for entity, char in self.HTML_ENTITIES.items():
            text = text.replace(entity, char)

        # 替换多个空格为单个空格
        text = re.sub(r'[ \t]+', ' ', text)

        # 替换多个换行为单个换行
        text = re.sub(r'\n\s*\n', '\n', text)

        # 移除首尾空白
        text = text.strip()

        # 移除每行首尾空白
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(line for line in lines if line)

        return text

    def truncate_text(self, text: Optional[str], max_length: int, suffix: str = '...') -> str:
        """
        截断文本

        Args:
            text: 原始文本
            max_length: 最大长度
            suffix: 截断后添加的后缀

        Returns:
            截断后的文本
        """
        if not text:
            return ''

        if len(text) <= max_length:
            return text

        return text[:max_length - len(suffix)] + suffix

    def validate_data(self, data: Dict[str, Any]) -> tuple:
        """
        验证必填字段

        Args:
            data: 待验证的数据字典

        Returns:
            (is_valid, errors)
            - is_valid: 是否有效
            - errors: 错误信息列表
        """
        errors = []

        for field in self.REQUIRED_FIELDS:
            value = data.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                errors.append(f"字段 '{field}' 为必填项")

        # 检查字段长度
        for field, max_length in self.MAX_LENGTHS.items():
            value = data.get(field)
            if value and isinstance(value, str) and len(value) > max_length:
                errors.append(
                    f"字段 '{field}' 长度超过限制 ({len(value)} > {max_length})"
                )

        return len(errors) == 0, errors

    def check_duplicate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        检测潜在重复数据（供 Pipeline 判断）

        注意：实际去重由数据库唯一约束处理

        Args:
            data: 待检查的数据

        Returns:
            包含重复检查结果的字典
        """
        return {
            'title': data.get('title', '').strip() if data.get('title') else '',
            'source_url': data.get('source_url', '').strip() if data.get('source_url') else '',
        }

    def clean_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        完整清洗流程

        依次执行：HTML 清洗、文本规范化、字段截断

        Args:
            item: 原始数据字典

        Returns:
            清洗后的数据字典
        """
        cleaned = {}

        for key, value in item.items():
            if value is None:
                cleaned[key] = ''  # None 转换为空字符串，便于后续验证
                continue

            if key in ['title', 'description', 'answer_content', 'answerer']:
                # HTML 清洗
                value = self.clean_html(value)
                # 文本规范化
                value = self.normalize_text(value)
                # 字段截断
                if key in self.MAX_LENGTHS:
                    value = self.truncate_text(value, self.MAX_LENGTHS[key])

            cleaned[key] = value

        return cleaned


class DuplicateChecker:
    """
    重复数据检测器

    用于在 Pipeline 中维护已处理的数据状态。
    """

    def __init__(self):
        self._seen_titles: set = set()
        self._seen_urls: set = set()
        self._duplicate_count: int = 0

    def is_duplicate(self, title: str, source_url: str) -> bool:
        """
        检查是否重复

        Args:
            title: 问题标题
            source_url: 来源链接

        Returns:
            是否为重复数据
        """
        # 标准化用于比较
        title_key = title.strip().lower()
        url_key = source_url.strip().lower()

        if title_key in self._seen_titles or url_key in self._seen_urls:
            self._duplicate_count += 1
            return True

        self._seen_titles.add(title_key)
        self._seen_urls.add(url_key)
        return False

    def get_duplicate_count(self) -> int:
        """
        获取重复数据数量

        Returns:
            重复数据计数
        """
        return self._duplicate_count

    def reset(self):
        """重置状态"""
        self._seen_titles.clear()
        self._seen_urls.clear()
        self._duplicate_count = 0


# 便捷函数
def clean_html(text: Optional[str]) -> str:
    """移除 HTML 标签"""
    return DataCleaner().clean_html(text)


def normalize_text(text: Optional[str]) -> str:
    """文本规范化"""
    return DataCleaner().normalize_text(text)


def clean_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """完整清洗流程"""
    return DataCleaner().clean_item(item)
