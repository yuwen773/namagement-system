# -*- coding: utf-8 -*-
"""
下厨房爬虫优化版

功能：
- 从列表页获取有效菜谱 ID
- 多线程并发爬取
- 429 错误智能重试
- 断点续传
"""

import os
import sys
import json
import time
import hashlib
import random
import threading
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

# Windows 控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from request_utils import RequestUtils, get_request_utils
from parser_utils import parse_recipe_detail, parse_recipe_list


class XiachufangSpiderOptimized:
    """下厨房爬虫优化版"""

    BASE_URL = "https://www.xiachufang.com"

    # 分类页面 URL 模板
    CATEGORY_URLS = [
        "/category/",
        "/explore/",
        "/recipe/",
    ]

    def __init__(
        self,
        output_dir: str = "output",
        download_images: bool = False,
        max_workers: int = 5,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
    ):
        """
        初始化爬虫

        Args:
            output_dir: 输出目录
            download_images: 是否下载图片
            max_workers: 最大并发线程数
            min_delay: 最小请求间隔（秒）
            max_delay: 最大请求间隔（秒）
        """
        self.output_dir = Path(output_dir)
        self.download_images = download_images
        self.max_workers = max_workers
        self.min_delay = min_delay
        self.max_delay = max_delay

        # 创建目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 线程锁
        self.lock = threading.Lock()
        self.request_lock = threading.Lock()

        # 统计数据
        self.stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            '429_errors': 0,
            'start_time': None,
            'end_time': None,
        }

        # 爬取结果
        self.recipes: List[Dict[str, Any]] = []
        self.failed_ids: Set[int] = set()
        self.crawled_ids: Set[int] = set()

        # 断点续传
        self.checkpoint_file = self.output_dir / "checkpoint.json"

    def load_checkpoint(self) -> Set[int]:
        """加载断点，返回已爬取的 ID 集合"""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('crawled_ids', []))
            except Exception:
                pass
        return set()

    def save_checkpoint(self):
        """保存断点"""
        with self.lock:
            data = {
                'crawled_ids': list(self.crawled_ids),
                'success_count': self.stats['success'],
                'failed_count': self.stats['failed'],
                'timestamp': datetime.now().isoformat(),
            }
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)

    def get_recipe_url(self, recipe_id: int) -> str:
        """构建菜谱详情页 URL"""
        return f"{self.BASE_URL}/recipe/{recipe_id}/"

    def crawl_with_retry(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        带重试的请求

        Args:
            url: 请求 URL
            max_retries: 最大重试次数

        Returns:
            HTML 内容，失败返回 None
        """
        for attempt in range(max_retries):
            try:
                # 请求延迟控制（线程安全）
                with self.request_lock:
                    delay = random.uniform(self.min_delay, self.max_delay)
                    time.sleep(delay)

                # 使用全局请求工具
                response = get_request_utils().get(url)
                return response.text

            except Exception as e:
                error_msg = str(e)

                # 429 错误特殊处理
                if '429' in error_msg:
                    with self.lock:
                        self.stats['429_errors'] += 1

                    # 等待时间递增
                    wait_time = (attempt + 1) * 30
                    print(f"[429] 触发限制，等待 {wait_time} 秒...")
                    time.sleep(wait_time)

                    if attempt < max_retries - 1:
                        continue
                    else:
                        return None

                # 其他错误
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return None

        return None

    def crawl_recipe(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """
        爬取单个菜谱（线程安全）

        Args:
            recipe_id: 菜谱 ID

        Returns:
            菜谱数据字典，失败返回 None
        """
        # 检查是否已爬取
        if recipe_id in self.crawled_ids:
            return None

        url = self.get_recipe_url(recipe_id)

        try:
            # 请求页面
            html = self.crawl_with_retry(url)
            if not html:
                with self.lock:
                    self.stats['failed'] += 1
                    self.failed_ids.add(recipe_id)
                return None

            # 解析数据
            recipe_data = parse_recipe_detail(html)

            # 验证必填字段
            if not recipe_data.get('name'):
                with self.lock:
                    self.stats['skipped'] += 1
                    self.crawled_ids.add(recipe_id)
                return None

            # 添加元数据
            recipe_data['recipe_id'] = recipe_id
            recipe_data['source_url'] = url
            recipe_data['crawled_at'] = datetime.now().isoformat()

            # 下载图片（可选）
            if self.download_images and recipe_data.get('image_url'):
                # 图片下载逻辑可以添加在这里
                pass

            with self.lock:
                self.stats['success'] += 1
                self.crawled_ids.add(recipe_id)

                # 定期保存断点
                if self.stats['success'] % 50 == 0:
                    self.save_checkpoint()

            thread_name = threading.current_thread().name
            print(f"[{thread_name}] [OK] {recipe_data['name']} (ID: {recipe_id})")

            return recipe_data

        except Exception as e:
            with self.lock:
                self.stats['failed'] += 1
                self.failed_ids.add(recipe_id)
            print(f"[{threading.current_thread().name}] [FAIL] ID {recipe_id}: {e}")
            return None

    def crawl_by_ids(
        self,
        recipe_ids: List[int],
        batch_size: int = 500,
        save_interval: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        多线程批量爬取

        Args:
            recipe_ids: 菜谱 ID 列表
            batch_size: 每批处理数量
            save_interval: 每隔多少条保存一次

        Returns:
            爬取的菜谱数据列表
        """
        self.stats['start_time'] = datetime.now()

        # 加载断点
        crawled = self.load_checkpoint()
        self.crawled_ids = crawled

        # 过滤已爬取的 ID
        remaining_ids = [rid for rid in recipe_ids if rid not in self.crawled_ids]
        total = len(remaining_ids)

        print(f"\n开始爬取，共 {total} 个菜谱（已跳过 {len(recipe_ids) - total} 个已爬取）")
        print(f"并发数: {self.max_workers}, 延迟: {self.min_delay}-{self.max_delay}秒")
        print("=" * 50)

        # 分批处理
        for i in range(0, len(remaining_ids), batch_size):
            batch = remaining_ids[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(remaining_ids) + batch_size - 1) // batch_size

            print(f"\n--- 批次 {batch_num}/{total_batches} ({len(batch)} 条) ---")

            # 多线程爬取
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.crawl_recipe, rid): rid for rid in batch}

                for j, future in enumerate(as_completed(futures), 1):
                    recipe_id = futures[future]
                    print(f"  进度: [{j}/{len(batch)}] ", end="", flush=True)

                    try:
                        recipe_data = future.result()
                        if recipe_data:
                            self.recipes.append(recipe_data)
                    except Exception as e:
                        print(f"  [异常] ID {recipe_id}: {e}")

            # 每批次保存
            self.save_data(f"batch_{batch_num}.json")
            self.save_checkpoint()

            # 显示进度
            print(f"\n当前统计: 成功={self.stats['success']}, 失败={self.stats['failed']}, 跳过={self.stats['skipped']}")

        self.stats['end_time'] = datetime.now()
        self.print_stats()

        return self.recipes

    def crawl_by_range(
        self,
        start_id: int,
        end_id: int,
        save_interval: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        按 ID 范围爬取

        Args:
            start_id: 起始 ID
            end_id: 结束 ID
            save_interval: 保存间隔

        Returns:
            爬取的菜谱数据列表
        """
        recipe_ids = list(range(start_id, end_id + 1))
        return self.crawl_by_ids(recipe_ids, save_interval=save_interval)

    def save_data(self, filename: str = None) -> str:
        """
        保存爬取的数据到 JSON 文件

        Args:
            filename: 文件名（不含目录）

        Returns:
            保存的文件路径
        """
        if not self.recipes:
            print("没有数据可保存")
            return ""

        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recipes_{timestamp}.json"

        save_path = self.output_dir / filename

        # 准备保存数据（处理 datetime 对象）
        stats_copy = self.stats.copy()
        stats_copy['start_time'] = stats_copy['start_time'].isoformat() if stats_copy.get('start_time') else None
        stats_copy['end_time'] = stats_copy['end_time'].isoformat() if stats_copy.get('end_time') else None

        output_data = {
            'metadata': {
                'total': len(self.recipes),
                'crawled_at': datetime.now().isoformat(),
                'stats': stats_copy,
            },
            'recipes': self.recipes
        }

        # 保存文件
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"数据已保存到: {save_path}")
        return str(save_path)

    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 50)
        print("爬取统计")
        print("=" * 50)
        print(f"成功: {self.stats['success']}")
        print(f"失败: {self.stats['failed']}")
        print(f"跳过: {self.stats['skipped']}")
        print(f"429 错误: {self.stats['429_errors']}")

        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            print(f"耗时: {duration:.2f} 秒 ({duration/60:.1f} 分钟)")
            if self.stats['success'] > 0:
                print(f"平均: {duration / self.stats['success']:.2f} 秒/条")

        print("=" * 50)


def main():
    """主函数"""
    spider = XiachufangSpiderOptimized(
        max_workers=5,      # 5个并发线程
        min_delay=1.0,      # 最小延迟1秒
        max_delay=3.0,      # 最大延迟3秒
        download_images=False,
    )

    try:
        # 测试爬取 100 条
        print("测试模式：爬取 ID 100000-100099")
        spider.crawl_by_range(start_id=100000, end_id=100099)

        # 保存数据
        spider.save_data("test_recipes.json")

    finally:
        # 保存最终断点
        spider.save_checkpoint()


if __name__ == "__main__":
    main()
