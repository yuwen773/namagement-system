"""
Django管理命令 - CSV数据导入
使用: python manage.py import_csv
"""
import os
import csv
import re
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List, Tuple, Any

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from products.models import Product, CrawlLog


class ProductCSVImporter:
    """商品CSV数据导入器"""

    # CSV字段到数据库字段的映射
    FIELD_MAPPING = {
        '商品ID': 'product_id',
        '商品标题': 'title',
        '价格': 'price',
        '价格单位': 'price_unit',
        '价格描述': 'price_desc',
        '卖家昵称': 'seller_nick',
        '店铺名称': 'shop',
        '店铺标签': 'shop_tags',
        '销量': 'sales',
        '地区': 'region',
        '标签': 'tags',
        '商品属性': 'product_attributes',
        '图片链接': 'image_url',
        '商品链接': 'detail_url',
    }

    def __init__(self, data_dir: str = None, batch_size: int = 100):
        """
        初始化导入器

        Args:
            data_dir: CSV文件目录路径
            batch_size: 批量插入大小
        """
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent.parent.parent / 'data'
        self.batch_size = batch_size
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_rows': 0,
            'success_count': 0,
            'skip_count': 0,
            'error_count': 0,
            'errors': []
        }

    def find_csv_files(self) -> List[Path]:
        """查找data目录下所有CSV文件"""
        csv_files = list(self.data_dir.glob('*.csv'))
        return sorted(csv_files)

    def parse_sales(self, sales_str: str) -> int:
        """
        解析销量字符串，提取数字

        Examples:
            "65人付款" -> 65
            "2000+人付款" -> 2000
            "" -> 0
        """
        if not sales_str:
            return 0

        # 提取所有数字
        match = re.search(r'(\d+)', str(sales_str))
        if match:
            return int(match.group(1))
        return 0

    def parse_price(self, price_str: str) -> Decimal:
        """
        解析价格字符串

        Args:
            price_str: 价格字符串

        Returns:
            Decimal对象
        """
        if not price_str:
            return Decimal('0.00')

        try:
            # 移除可能的货币符号和空格
            price_clean = re.sub(r'[^\d.]', '', str(price_str))
            return Decimal(price_clean) if price_clean else Decimal('0.00')
        except (InvalidOperation, ValueError):
            return Decimal('0.00')

    def parse_attributes(self, attr_str: str) -> Dict[str, Any]:
        """
        解析商品属性字符串为JSON

        Example input:
            "出售状态:现货 | 版本类型:日版 | 品牌:Bandai/万代"

        Returns:
            Dict: {'出售状态': '现货', '版本类型': '日版', '品牌': 'Bandai/万代'}
        """
        if not attr_str:
            return {}

        result = {}
        try:
            # 分割属性对
            pairs = str(attr_str).split('|')
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    result[key.strip()] = value.strip()
        except Exception:
            # 如果解析失败，返回原始字符串
            result = {'raw': str(attr_str)}

        return result

    def parse_region(self, region_str: str) -> str:
        """格式化地区字符串"""
        if not region_str:
            return ''
        return str(region_str).strip()

    def generate_batch_no(self) -> str:
        """生成批次号"""
        return f"IMPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def clean_row_data(self, row: Dict[str, str]) -> Dict[str, str]:
        """
        清洗CSV行数据，填充缺失的必填字段

        Args:
            row: 原始CSV行数据

        Returns:
            清洗后的行数据
        """
        cleaned = row.copy()

        # 清除所有字段的空白字符
        for key, value in cleaned.items():
            if value:
                cleaned[key] = str(value).strip()

        # 数据清洗：填充缺失的必填字段
        if not cleaned.get('商品标题') or not cleaned.get('商品标题').strip():
            # 尝试从其他字段组合生成标题
            title_parts = []
            if cleaned.get('商品属性'):
                attrs = self.parse_attributes(cleaned['商品属性'])
                if attrs.get('品牌'):
                    title_parts.append(attrs['品牌'])
                if attrs.get('款式类型'):
                    title_parts.append(attrs['款式类型'])
            if cleaned.get('商品ID'):
                title_parts.append(f"ID:{cleaned['商品ID']}")
            if cleaned.get('类目'):
                title_parts.append(cleaned['类目'])

            cleaned['商品标题'] = ' '.join(title_parts) if title_parts else f"潮玩商品 {cleaned.get('商品ID', '')}"

        if not cleaned.get('店铺名称') or not cleaned.get('店铺名称').strip():
            # 使用卖家昵称或默认值
            cleaned['店铺名称'] = cleaned.get('卖家昵称') or '潮玩店铺'

        if not cleaned.get('商品链接') or not cleaned.get('商品链接').strip():
            # 从商品ID生成链接
            product_id = cleaned.get('商品ID')
            if product_id:
                cleaned['商品链接'] = f"https://detail.tmall.com/item.htm?id={product_id}"
            else:
                cleaned['商品链接'] = "https://www.tmall.com/"

        return cleaned

    def row_to_product_dict(self, row: Dict[str, str], batch_no: str) -> Dict[str, Any]:
        """
        将CSV行数据转换为Product模型字典

        Args:
            row: CSV行数据
            batch_no: 批次号

        Returns:
            Product模型字段字典
        """
        # 先进行数据清洗
        row = self.clean_row_data(row)

        product_data = {}

        # 基础字段映射
        for csv_field, model_field in self.FIELD_MAPPING.items():
            if csv_field in row:
                value = row[csv_field]

                # 特殊字段处理
                if model_field == 'price':
                    product_data[model_field] = self.parse_price(value)
                elif model_field == 'sales':
                    product_data[model_field] = self.parse_sales(value)
                elif model_field == 'product_attributes':
                    product_data[model_field] = self.parse_attributes(value)
                elif model_field == 'region':
                    product_data[model_field] = self.parse_region(value)
                elif model_field == 'detail_url':
                    # 截断过长的URL到1000字符
                    url_value = str(value).strip() if value else ''
                    product_data[model_field] = url_value[:1000] if url_value else 'https://www.tmall.com/'
                elif model_field == 'image_url':
                    # 截断过长的图片URL
                    img_value = str(value).strip() if value else ''
                    product_data[model_field] = img_value[:500] if img_value else ''
                elif model_field == 'title':
                    # 截断过长的标题
                    title_value = str(value).strip() if value else ''
                    product_data[model_field] = title_value[:500] if title_value else '未命名商品'
                elif model_field == 'shop':
                    # 截断过长的店铺名
                    shop_value = str(value).strip() if value else ''
                    product_data[model_field] = shop_value[:200] if shop_value else '潮玩店铺'
                else:
                    # 普通字段直接赋值
                    product_data[model_field] = str(value).strip() if value else None

        # 添加系统字段
        product_data['batch_no'] = batch_no
        product_data['crawl_time'] = timezone.now()

        # 设置默认值
        if 'brand' not in product_data or not product_data.get('brand'):
            # 尝试从商品属性中提取品牌
            attrs = product_data.get('product_attributes', {})
            if isinstance(attrs, dict) and '品牌' in attrs:
                product_data['brand'] = attrs['品牌']

        return product_data

    def validate_product_data(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        验证产品数据

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # 必填字段检查
        if not data.get('title'):
            errors.append('商品标题不能为空')

        if not data.get('shop'):
            errors.append('店铺名称不能为空')

        if not data.get('detail_url'):
            errors.append('商品链接不能为空')

        return len(errors) == 0, errors

    def is_empty_row(self, row: Dict[str, str]) -> bool:
        """
        检查是否为空行

        Args:
            row: CSV行数据

        Returns:
            是否为空行
        """
        if not row:
            return True
        # 检查所有字段是否都为空
        return all(not value or not str(value).strip() for value in row.values())

    def detect_and_fix_csv(self, csv_file: Path) -> List[Dict[str, str]]:
        """
        检测并修复CSV文件，自动添加缺失的表头

        Args:
            csv_file: CSV文件路径

        Returns:
            解析后的行数据列表
        """
        # 标准表头
        standard_headers = [
            '商品ID', '商品标题', '价格', '价格单位', '价格描述',
            '卖家昵称', '店铺名称', '店铺标签', '销量', '地区',
            '标签', '商品属性', '图片链接', '商品链接'
        ]

        rows = []
        for encoding in ['utf-8-sig', 'utf-8', 'gbk', 'gb2312']:
            try:
                with open(csv_file, 'r', encoding=encoding) as f:
                    content = f.read()
                    # 按行分割
                    lines = content.strip().split('\n')
                    if not lines:
                        continue

                    # 检查第一行是否是标准表头
                    first_line = lines[0].strip()
                    is_header = False

                    # 检查是否包含标准表头关键字
                    if first_line.startswith('﻿'):
                        first_line = first_line[1:]  # 移除BOM

                    # 解析第一行
                    first_fields = [f.strip() for f in first_line.split(',')]

                    # 检查是否是标准表头
                    if any(field in standard_headers for field in first_fields if field):
                        is_header = True
                    else:
                        # 检查第一个字段是否看起来像商品ID（纯数字或长数字）
                        if first_fields and first_fields[0].isdigit() and len(first_fields[0]) > 8:
                            is_header = False  # 这是数据，不是表头
                        else:
                            is_header = True  # 假设是表头

                    # 如果不是标准表头，则添加标准表头
                    if not is_header:
                        lines = [','.join(standard_headers)] + lines

                    # 使用 csv.DictReader 解析
                    from io import StringIO
                    csv_content = '\n'.join(lines)
                    reader = csv.DictReader(StringIO(csv_content))
                    rows = list(reader)
                    break

            except (UnicodeDecodeError, Exception):
                continue

        return rows

    def import_csv_file(self, csv_file: Path, batch_no: str) -> Tuple[int, int, int]:
        """
        导入单个CSV文件

        Returns:
            (success_count, skip_count, error_count)
        """
        success_count = 0
        skip_count = 0
        error_count = 0

        try:
            # 使用新的检测和修复方法
            rows = self.detect_and_fix_csv(csv_file)

            if not rows:
                raise Exception("无法读取CSV文件，编码不支持或文件为空")

            self.stats['total_rows'] += len(rows)

            # 批量导入
            batch_products = []

            for row in rows:
                try:
                    # 跳过空行
                    if self.is_empty_row(row):
                        skip_count += 1
                        continue

                    # 转换为产品数据
                    product_data = self.row_to_product_dict(row, batch_no)

                    # 数据验证
                    is_valid, errors = self.validate_product_data(product_data)

                    if not is_valid:
                        skip_count += 1
                        self.stats['errors'].append({
                            'file': csv_file.name,
                            'row': row.get('商品ID', 'unknown'),
                            'errors': errors
                        })
                        continue

                    # 直接创建新记录（不检查重复，允许同一product_id有多条记录）
                    batch_products.append(Product(**product_data))

                    # 批量保存
                    if len(batch_products) >= self.batch_size:
                        Product.objects.bulk_create(batch_products, batch_size=self.batch_size)
                        success_count += len(batch_products)
                        batch_products = []

                except Exception as e:
                    error_count += 1
                    self.stats['errors'].append({
                        'file': csv_file.name,
                        'row': row.get('商品ID', 'unknown'),
                        'error': str(e)
                    })

            # 保存剩余记录
            if batch_products:
                Product.objects.bulk_create(
                    batch_products,
                    update_fields=[f for f in self.FIELD_MAPPING.values()] + ['batch_no', 'crawl_time'],
                    ignore_conflicts=True
                )
                success_count += len(batch_products)

        except Exception as e:
            self.stats['errors'].append({
                'file': csv_file.name,
                'error': f"文件读取失败: {str(e)}"
            })
            error_count += 1

        return success_count, skip_count, error_count

    def import_all(self) -> Dict[str, Any]:
        """
        导入data目录下所有CSV文件

        Returns:
            导入统计信息
        """
        csv_files = self.find_csv_files()
        self.stats['total_files'] = len(csv_files)

        if not csv_files:
            return {
                'status': 'no_files',
                'message': f'在 {self.data_dir} 目录下未找到CSV文件',
                'stats': self.stats
            }

        batch_no = self.generate_batch_no()

        print(f"找到 {len(csv_files)} 个CSV文件")
        print(f"批次号: {batch_no}")
        print("-" * 60)

        for csv_file in csv_files:
            print(f"正在处理: {csv_file.name}")
            success, skip, error = self.import_csv_file(csv_file, batch_no)

            self.stats['processed_files'] += 1
            self.stats['success_count'] += success
            self.stats['skip_count'] += skip
            self.stats['error_count'] += error

            print(f"  成功: {success}, 跳过: {skip}, 错误: {error}")
            print()

        # 创建采集日志
        self._create_crawl_log(batch_no)

        return {
            'status': 'completed',
            'batch_no': batch_no,
            'stats': self.stats
        }

    def _create_crawl_log(self, batch_no: str):
        """创建采集日志记录"""
        try:
            CrawlLog.objects.create(
                task_id=f"IMPORT_{batch_no}",
                status=CrawlLog.Status.SUCCESS,
                mode='import',
                source_type=CrawlLog.SourceType.DEMO,
                start_time=timezone.now(),
                end_time=timezone.now(),
                items_collected=self.stats['success_count'],
                items_success=self.stats['success_count'],
                items_failed=self.stats['error_count'] + self.stats['skip_count'],
                log_content=f"CSV批量导入\n批次号: {batch_no}\n处理文件: {self.stats['processed_files']}/{self.stats['total_files']}\n成功: {self.stats['success_count']}\n跳过: {self.stats['skip_count']}\n错误: {self.stats['error_count']}"
            )
        except Exception as e:
            print(f"WARNING: Failed to create crawl log: {str(e)}")


class Command(BaseCommand):
    help = '从data目录导入CSV商品数据到数据库'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            type=str,
            help='CSV文件所在目录（默认: backend/data）'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='批量插入大小（默认: 100）'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='试运行，不实际导入数据'
        )

    def handle(self, *args, **options):
        data_dir = options.get('dir')
        batch_size = options.get('batch_size', 100)
        dry_run = options.get('dry_run', False)

        self.stdout.write(self.style.SUCCESS('开始CSV数据导入'))

        if dry_run:
            self.stdout.write(self.style.WARNING('试运行模式 - 不会实际导入数据'))

        try:
            importer = ProductCSVImporter(data_dir=data_dir, batch_size=batch_size)

            if not dry_run:
                # 不使用外层事务，让每个文件的导入独立处理
                result = importer.import_all()

                # 打印结果
                self._print_results(result)
            else:
                # 试运行 - 只显示将要导入的数据
                csv_files = importer.find_csv_files()
                self.stdout.write(f"找到 {len(csv_files)} 个CSV文件:")
                for f in csv_files:
                    self.stdout.write(f"  - {f.name}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'导入失败: {str(e)}'))
            raise CommandError(str(e))

    def _print_results(self, result: Dict[str, Any]):
        """打印导入结果"""
        stats = result['stats']

        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('导入完成'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f"批次号: {result['batch_no']}")
        self.stdout.write(f"处理文件: {stats['processed_files']}/{stats['total_files']}")
        self.stdout.write(f"总行数: {stats['total_rows']}")
        self.stdout.write(self.style.SUCCESS(f"成功导入: {stats['success_count']}"))
        self.stdout.write(self.style.WARNING(f"跳过记录: {stats['skip_count']}"))
        self.stdout.write(self.style.ERROR(f"错误记录: {stats['error_count']}"))

        if stats['errors']:
            self.stdout.write(self.style.ERROR('\n错误详情:'))
            for err in stats['errors'][:10]:  # 只显示前10个错误
                row = err.get('row', '')
                error_msg = err.get('errors', err.get('error', ''))
                self.stdout.write(self.style.ERROR(f"  [{err['file']}] {row}: {error_msg}"))

            if len(stats['errors']) > 10:
                self.stdout.write(self.style.ERROR(f"  ... 还有 {len(stats['errors']) - 10} 个错误"))

        self.stdout.write(self.style.SUCCESS('=' * 60))
