"""
数据导入服务 - 提供Web API调用的导入功能
"""
import os
import csv
import re
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import threading

from django.db import transaction
from django.utils import timezone
from django.conf import settings

from products.models import Product, CrawlLog


# 全局导入任务状态
_import_tasks = {}
_task_lock = threading.Lock()


class ProductImportService:
    """商品数据导入服务 - 支持异步导入和进度追踪"""

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

    @classmethod
    def get_import_tasks(cls) -> List[Dict]:
        """获取所有导入任务状态"""
        with _task_lock:
            return list(_import_tasks.values())

    @classmethod
    def get_import_task(cls, task_id: str) -> Optional[Dict]:
        """获取指定任务状态"""
        with _task_lock:
            return _import_tasks.get(task_id)

    @classmethod
    def _update_task_status(cls, task_id: str, **kwargs):
        """更新任务状态"""
        with _task_lock:
            if task_id in _import_tasks:
                _import_tasks[task_id].update(kwargs)
                _import_tasks[task_id]['updated_at'] = timezone.now().isoformat()

    @classmethod
    def parse_sales(cls, sales_str: str) -> int:
        """解析销量字符串"""
        if not sales_str:
            return 0
        match = re.search(r'(\d+)', str(sales_str))
        return int(match.group(1)) if match else 0

    @classmethod
    def parse_price(cls, price_str: str) -> Decimal:
        """解析价格字符串"""
        if not price_str:
            return Decimal('0.00')
        try:
            price_clean = re.sub(r'[^\d.]', '', str(price_str))
            return Decimal(price_clean) if price_clean else Decimal('0.00')
        except (InvalidOperation, ValueError):
            return Decimal('0.00')

    @classmethod
    def parse_attributes(cls, attr_str: str) -> Dict[str, Any]:
        """解析商品属性字符串"""
        if not attr_str:
            return {}
        result = {}
        try:
            pairs = str(attr_str).split('|')
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    result[key.strip()] = value.strip()
        except Exception:
            result = {'raw': str(attr_str)}
        return result

    @classmethod
    def row_to_product_dict(cls, row: Dict[str, str], batch_no: str) -> Dict[str, Any]:
        """将CSV行转换为产品数据字典"""
        product_data = {}

        for csv_field, model_field in cls.FIELD_MAPPING.items():
            if csv_field in row:
                value = row[csv_field]

                if model_field == 'price':
                    product_data[model_field] = cls.parse_price(value)
                elif model_field == 'sales':
                    product_data[model_field] = cls.parse_sales(value)
                elif model_field == 'product_attributes':
                    product_data[model_field] = cls.parse_attributes(value)
                elif model_field == 'region':
                    product_data[model_field] = str(value).strip() if value else ''
                else:
                    product_data[model_field] = str(value).strip() if value else None

        product_data['batch_no'] = batch_no
        product_data['crawl_time'] = timezone.now()

        # 从属性中提取品牌
        if not product_data.get('brand'):
            attrs = product_data.get('product_attributes', {})
            if isinstance(attrs, dict) and '品牌' in attrs:
                product_data['brand'] = attrs['品牌']

        return product_data

    @classmethod
    def validate_product_data(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证产品数据"""
        errors = []
        if not data.get('title'):
            errors.append('商品标题不能为空')
        if not data.get('shop'):
            errors.append('店铺名称不能为空')
        if not data.get('detail_url'):
            errors.append('商品链接不能为空')
        return len(errors) == 0, errors

    @classmethod
    def find_csv_files(cls, data_dir: str = None) -> List[Path]:
        """查找所有CSV文件"""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / 'data'
        else:
            data_dir = Path(data_dir)

        if not data_dir.exists():
            return []

        return sorted(data_dir.glob('*.csv'))

    @classmethod
    def import_csv_file(cls, csv_file: Path, batch_no: str, task_id: str) -> Dict[str, int]:
        """导入单个CSV文件"""
        success_count = 0
        skip_count = 0
        error_count = 0

        try:
            # 尝试不同编码
            rows = None
            for encoding in ['utf-8-sig', 'utf-8', 'gbk', 'gb2312']:
                try:
                    with open(csv_file, 'r', encoding=encoding) as f:
                        rows = list(csv.DictReader(f))
                    break
                except UnicodeDecodeError:
                    continue

            if rows is None:
                raise Exception("不支持的文件编码")

            total_rows = len(rows)
            batch_products = []

            for idx, row in enumerate(rows):
                try:
                    product_data = cls.row_to_product_dict(row, batch_no)
                    is_valid, errors = cls.validate_product_data(product_data)

                    if not is_valid:
                        skip_count += 1
                        continue

                    # 检查是否存在
                    product_id = product_data.get('product_id')
                    if product_id:
                        existing = Product.objects.filter(product_id=product_id).first()
                        if existing:
                            for key, value in product_data.items():
                                setattr(existing, key, value)
                            batch_products.append(existing)
                        else:
                            batch_products.append(Product(**product_data))
                    else:
                        batch_products.append(Product(**product_data))

                    # 批量保存（每100条）
                    if len(batch_products) >= 100:
                        Product.objects.bulk_create(
                            batch_products,
                            update_fields=[f for f in cls.FIELD_MAPPING.values()] + ['batch_no', 'crawl_time'],
                            ignore_conflicts=True
                        )
                        success_count += len(batch_products)
                        batch_products = []

                    # 更新进度
                    if idx % 50 == 0:
                        progress = int((idx / total_rows) * 100)
                        cls._update_task_status(
                            task_id,
                            current_file=csv_file.name,
                            progress=progress
                        )

                except Exception as e:
                    error_count += 1

            # 保存剩余记录
            if batch_products:
                Product.objects.bulk_create(
                    batch_products,
                    update_fields=[f for f in cls.FIELD_MAPPING.values()] + ['batch_no', 'crawl_time'],
                    ignore_conflicts=True
                )
                success_count += len(batch_products)

        except Exception as e:
            error_count += 1

        return {'success': success_count, 'skip': skip_count, 'error': error_count}

    @classmethod
    def import_all_async(cls, task_id: str, data_dir: str = None) -> str:
        """
        异步导入所有CSV文件（在后台线程中执行）

        Args:
            task_id: 任务ID
            data_dir: CSV文件目录

        Returns:
            任务ID
        """
        def run_import():
            try:
                cls._update_task_status(task_id, status='running')

                csv_files = cls.find_csv_files(data_dir)

                if not csv_files:
                    cls._update_task_status(
                        task_id,
                        status='failed',
                        error='未找到CSV文件'
                    )
                    return

                batch_no = f"IMPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                total_success = 0
                total_skip = 0
                total_error = 0

                for csv_file in csv_files:
                    result = cls.import_csv_file(csv_file, batch_no, task_id)
                    total_success += result['success']
                    total_skip += result['skip']
                    total_error += result['error']

                # 创建采集日志
                CrawlLog.objects.create(
                    task_id=task_id,
                    status=CrawlLog.Status.SUCCESS,
                    mode='import',
                    source_type=CrawlLog.SourceType.DEMO,
                    start_time=timezone.now(),
                    end_time=timezone.now(),
                    items_collected=total_success,
                    items_success=total_success,
                    items_failed=total_skip + total_error,
                    log_content=f"CSV批量导入\n批次号: {batch_no}\n成功: {total_success}\n跳过: {total_skip}\n错误: {total_error}"
                )

                cls._update_task_status(
                    task_id,
                    status='completed',
                    progress=100,
                    batch_no=batch_no,
                    total_success=total_success,
                    total_skip=total_skip,
                    total_error=total_error
                )

            except Exception as e:
                cls._update_task_status(
                    task_id,
                    status='failed',
                    error=str(e)
                )

        # 创建任务记录
        with _task_lock:
            _import_tasks[task_id] = {
                'task_id': task_id,
                'status': 'pending',
                'progress': 0,
                'created_at': timezone.now().isoformat(),
                'updated_at': timezone.now().isoformat()
            }

        # 在后台线程运行
        thread = threading.Thread(target=run_import, daemon=True)
        thread.start()

        return task_id

    @classmethod
    def start_import(cls, data_dir: str = None) -> str:
        """
        启动导入任务

        Returns:
            任务ID
        """
        task_id = f"IMPORT_{datetime.now().strftime('%Y%m%d%H%M%S_%f')}"
        return cls.import_all_async(task_id, data_dir)
