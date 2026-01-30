# -*- coding: utf-8 -*-
"""
下厨房爬虫主脚本

功能：
- 爬取菜谱数据
- 下载图片
- 保存为 JSON 格式
- 进度跟踪和日志记录
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Windows 控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from request_utils import RequestUtils, get_request_utils
from parser_utils import parse_recipe_detail, parse_recipe_list


class XiachufangSpider:
    """下厨房爬虫类"""

    BASE_URL = "https://www.xiachufang.com"

    # 初始菜谱 ID（用于测试）
    INITIAL_RECIPE_IDS = list(range(100000, 100100))

    def __init__(
        self,
        output_dir: str = "output",
        images_dir: str = "images",
        download_images: bool = True
    ):
        """
        初始化爬虫

        Args:
            output_dir: 输出目录（JSON 文件）
            images_dir: 图片保存目录
            download_images: 是否下载图片
        """
        self.output_dir = Path(output_dir)
        self.images_dir = Path(images_dir)
        self.download_images = download_images
        self.request_utils: Optional[RequestUtils] = None

        # 创建目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

        # 统计数据
        self.stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'end_time': None,
        }

        # 爬取结果
        self.recipes: List[Dict[str, Any]] = []

    def get_request_utils(self) -> RequestUtils:
        """获取请求工具实例"""
        if self.request_utils is None:
            self.request_utils = get_request_utils()
        return self.request_utils

    def get_recipe_url(self, recipe_id: int) -> str:
        """构建菜谱详情页 URL"""
        return f"{self.BASE_URL}/recipe/{recipe_id}/"

    def download_image(self, image_url: str, recipe_id: int) -> Optional[str]:
        """
        下载图片

        Args:
            image_url: 图片 URL
            recipe_id: 菜谱 ID

        Returns:
            本地保存路径（相对于 images 目录）
        """
        if not image_url or not self.download_images:
            return None

        try:
            # 生成文件名
            url_hash = hashlib.md5(image_url.encode()).hexdigest()
            ext = image_url.split('.')[-1].split('?')[0]
            if ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                ext = 'jpg'

            filename = f"{recipe_id}_{url_hash[:8]}.{ext}"
            save_path = self.images_dir / filename

            # 如果图片已存在，跳过下载
            if save_path.exists():
                return f"images/{filename}"

            # 下载图片
            if self.get_request_utils().download_image(image_url, str(save_path)):
                return f"images/{filename}"

        except Exception as e:
            print(f"下载图片失败: {image_url}, 错误: {e}")

        return None

    def crawl_recipe(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """
        爬取单个菜谱

        Args:
            recipe_id: 菜谱 ID

        Returns:
            菜谱数据字典，失败返回 None
        """
        url = self.get_recipe_url(recipe_id)

        try:
            # 请求页面
            response = self.get_request_utils().get(url)
            html = response.text

            # 解析数据
            recipe_data = parse_recipe_detail(html)

            # 验证必填字段
            if not recipe_data.get('name'):
                print(f"菜谱 {recipe_id} 没有名称，跳过")
                self.stats['skipped'] += 1
                return None

            # 添加元数据
            recipe_data['recipe_id'] = recipe_id
            recipe_data['source_url'] = url
            recipe_data['crawled_at'] = datetime.now().isoformat()

            # 下载图片
            if recipe_data.get('image_url'):
                local_image_path = self.download_image(
                    recipe_data['image_url'],
                    recipe_id
                )
                if local_image_path:
                    recipe_data['local_image_path'] = local_image_path

            print(f"[OK] 成功爬取菜谱: {recipe_data['name']} (ID: {recipe_id})")
            self.stats['success'] += 1

            return recipe_data

        except Exception as e:
            print(f"[FAIL] 爬取失败: 菜谱 ID {recipe_id}, 错误: {e}")
            self.stats['failed'] += 1
            return None

    def crawl_by_ids(
        self,
        recipe_ids: List[int],
        batch_size: int = 50,
        save_interval: int = 10
    ) -> List[Dict[str, Any]]:
        """
        按菜谱 ID 批量爬取

        Args:
            recipe_ids: 菜谱 ID 列表
            batch_size: 每批处理数量
            save_interval: 每隔多少条保存一次

        Returns:
            爬取的菜谱数据列表
        """
        self.stats['start_time'] = datetime.now()
        total = len(recipe_ids)

        print(f"\n开始爬取，共 {total} 个菜谱")
        print("=" * 50)

        for i, recipe_id in enumerate(recipe_ids, 1):
            print(f"[{i}/{total}] ", end="")

            recipe_data = self.crawl_recipe(recipe_id)
            if recipe_data:
                self.recipes.append(recipe_data)

            # 定期保存
            if i % save_interval == 0:
                self.save_data(f"batch_{i}.json")
                print(f"已保存 {i} 条数据...")

        self.stats['end_time'] = datetime.now()
        self.print_stats()

        return self.recipes

    def crawl_by_range(
        self,
        start_id: int,
        end_id: int,
        save_interval: int = 10
    ) -> List[Dict[str, Any]]:
        """
        按ID范围爬取

        Args:
            start_id: 起始 ID
            end_id: 结束 ID
            save_interval: 保存间隔

        Returns:
            爬取的菜谱数据列表
        """
        recipe_ids = list(range(start_id, end_id + 1))
        return self.crawl_by_ids(recipe_ids, save_interval=save_interval)

    def crawl_test(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        测试爬取（少量数据）

        Args:
            count: 爬取数量

        Returns:
            爬取的菜谱数据列表
        """
        print(f"\n测试模式：爬取 {count} 条数据")
        print("=" * 50)

        recipe_ids = self.INITIAL_RECIPE_IDS[:count]
        return self.crawl_by_ids(recipe_ids, save_interval=count)

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

        # 准备保存数据
        output_data = {
            'metadata': {
                'total': len(self.recipes),
                'crawled_at': datetime.now().isoformat(),
                'stats': self.stats,
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

        if self.stats['start_time'] and self.stats['end_time']:
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            print(f"耗时: {duration:.2f} 秒")
            if self.stats['success'] > 0:
                print(f"平均: {duration / self.stats['success']:.2f} 秒/条")

        print("=" * 50)

    def close(self):
        """关闭资源"""
        if self.request_utils:
            self.request_utils.close()


def main():
    """主函数 - 测试模式"""
    spider = XiachufangSpider()

    try:
        # 测试爬取 10 条数据
        spider.crawl_test(count=10)

        # 保存数据
        spider.save_data("test_recipes.json")

    finally:
        spider.close()


if __name__ == "__main__":
    main()
