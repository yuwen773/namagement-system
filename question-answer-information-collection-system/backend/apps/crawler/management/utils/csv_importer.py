"""
CSV 数据导入工具类

用于将 360 问答 CSV 数据导入到 Django 数据库。
"""
import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

from django.db import transaction, DatabaseError
from django.utils import timezone

from apps.crawler.models import Question


class CSVImportResult:
    """导入结果统计"""
    def __init__(self):
        self.total = 0
        self.success = 0
        self.skipped = 0
        self.failed = 0
        self.errors: List[str] = []

    def to_dict(self) -> Dict:
        return {
            'total': self.total,
            'success': self.success,
            'skipped': self.skipped,
            'failed': self.failed,
            'errors': self.errors[:10]  # 只返回前10个错误
        }

    def __str__(self) -> str:
        return (
            f"总计: {self.total} | "
            f"成功: {self.success} | "
            f"跳过: {self.skipped} | "
            f"失败: {self.failed}"
        )


class CSVImporter:
    """360问答 CSV 数据导入器"""

    # CSV 字段映射到数据库字段
    FIELD_MAPPING = {
        'pn': 'crawl_page',
        'id': 'question_id',
        'title': 'title',
        'category': 'category',
        'answer_count': 'answer_count',
        'time': 'publish_time',
        'location': 'location',
    }

    def __init__(self, file_path: str, batch_size: int = 100):
        """
        初始化导入器

        Args:
            file_path: CSV 文件路径
            batch_size: 批量插入大小
        """
        self.file_path = file_path
        self.batch_size = batch_size
        self.result = CSVImportResult()

    def validate_file(self) -> bool:
        """验证 CSV 文件是否存在且格式正确"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"CSV 文件不存在: {self.file_path}")

        if not self.file_path.endswith('.csv'):
            raise ValueError("文件必须是 CSV 格式")

        # 检查文件是否可读
        try:
            with open(self.file_path, 'r', encoding='utf-8-sig') as f:
                # 尝试读取第一行
                f.readline()
        except Exception as e:
            raise IOError(f"无法读取 CSV 文件: {e}")

        return True

    def count_total_rows(self) -> int:
        """统计 CSV 文件总行数（不包含表头）"""
        with open(self.file_path, 'r', encoding='utf-8-sig') as f:
            return sum(1 for _ in f) - 1  # 减去表头

    def parse_date(self, date_str: str) -> Optional[datetime.date]:
        """
        解析日期字符串

        支持格式:
        - YYYY.MM.DD (2025.11.21)
        - YYYY-MM-DD (2025-11-21)

        Args:
            date_str: 日期字符串

        Returns:
            datetime.date 对象或 None
        """
        if not date_str or date_str.strip() == '':
            return None

        # 尝试不同的日期格式
        formats = ['%Y.%m.%d', '%Y-%m-%d']

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue

        return None

    def clean_category(self, category: str) -> Optional[str]:
        """
        清理分类字段

        去除方括号: [影视] -> 影视

        Args:
            category: 原始分类字符串

        Returns:
            清理后的分类字符串
        """
        if not category or category.strip() == '':
            return None

        # 使用正则去除方括号
        cleaned = re.sub(r'[\[\]]', '', category.strip())
        return cleaned if cleaned else None

    def generate_source_url(self, question_id: str) -> str:
        """
        生成来源链接

        Args:
            question_id: 问题ID

        Returns:
            完整的 URL
        """
        return f"https://wenda.so.com/q/{question_id}"

    def generate_description(self, title: str) -> str:
        """
        生成描述（从标题复制）

        Args:
            title: 问题标题

        Returns:
            描述内容（最多200字符）
        """
        if not title:
            return ""
        return title[:200]

    def transform_row(self, row: Dict[str, str]) -> Optional[Dict]:
        """
        转换单行 CSV 数据为模型字段

        Args:
            row: CSV 行数据

        Returns:
            转换后的字段字典，如果转换失败返回 None
        """
        try:
            # 映射基础字段
            data = {}

            # 处理 question_id (必填)
            question_id = row.get('id', '').strip()
            if not question_id:
                return None
            data['question_id'] = question_id

            # 处理 title (必填)
            title = row.get('title', '').strip()
            if not title:
                return None
            data['title'] = title

            # 处理 description (生成)
            data['description'] = self.generate_description(title)

            # 处理 category (清理)
            category = row.get('category', '')
            if category:
                data['category'] = self.clean_category(category)

            # 处理 publish_time (解析日期)
            time_str = row.get('time', '')
            if time_str:
                data['publish_time'] = self.parse_date(time_str)

            # 处理 location
            location = row.get('location', '').strip()
            if location:
                data['location'] = location

            # 处理 answer_count
            answer_count = row.get('answer_count', '0')
            try:
                data['answer_count'] = int(answer_count) if answer_count else 0
            except ValueError:
                data['answer_count'] = 0

            # 处理 crawl_page
            page_num = row.get('pn', '1')
            try:
                data['crawl_page'] = int(page_num) if page_num else 1
            except ValueError:
                data['crawl_page'] = 1

            # 生成 source_url (必填，唯一)
            data['source_url'] = self.generate_source_url(question_id)

            return data

        except Exception as e:
            self.result.errors.append(f"数据转换失败 (行: {row}): {e}")
            return None

    def bulk_import(self, dry_run: bool = False, verbose: bool = False,
                   progress_callback=None) -> CSVImportResult:
        """
        批量导入数据

        Args:
            dry_run: 预览模式，不实际写入数据库
            verbose: 详细输出
            progress_callback: 进度回调函数

        Returns:
            CSVImportResult 导入结果
        """
        self.validate_file()
        self.result.total = self.count_total_rows()

        if verbose:
            print(f"开始导入 CSV 数据...")
            print(f"文件: {self.file_path}")
            print(f"总记录数: {self.result.total}")
            print(f"批量大小: {self.batch_size}")
            if dry_run:
                print(">>> 预览模式（不会写入数据库）")

        batch = []
        processed = 0

        with open(self.file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for row in reader:
                processed += 1

                # 转换数据
                data = self.transform_row(row)
                if data is None:
                    self.result.failed += 1
                    continue

                if dry_run:
                    # 预览模式：只计数，不插入
                    self.result.success += 1
                else:
                    # 添加到批次
                    batch.append(data)

                    # 批量插入
                    if len(batch) >= self.batch_size:
                        self._insert_batch(batch)
                        batch = []

                # 进度回调
                if progress_callback:
                    progress_callback(processed, self.result.total, self.result)

            # 插入剩余数据
            if batch and not dry_run:
                self._insert_batch(batch)

        return self.result

    def _insert_batch(self, batch: List[Dict]) -> None:
        """
        插入一批数据

        Args:
            batch: 数据列表
        """
        try:
            with transaction.atomic():
                # 使用 bulk_create 批量创建
                # 使用 get_or_create 处理重复数据
                for data in batch:
                    Question.objects.get_or_create(
                        question_id=data['question_id'],
                        defaults=data
                    )
                    self.result.success += 1

        except DatabaseError as e:
            # 逐条插入以处理部分失败的情况
            for data in batch:
                try:
                    Question.objects.get_or_create(
                        question_id=data['question_id'],
                        defaults=data
                    )
                    self.result.success += 1
                except Exception as e:
                    if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                        # 重复数据
                        self.result.skipped += 1
                    else:
                        self.result.failed += 1
                        self.result.errors.append(f"插入失败: {e}")
