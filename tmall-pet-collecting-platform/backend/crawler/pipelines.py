"""
数据处理管道
用于清洗、验证和批量存储爬虫采集的数据
"""
import logging
from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any

from django.utils import timezone
from products.models import Product

logger = logging.getLogger('crawler')


class DataCleaningPipeline:
    """
    数据清洗管道

    功能：
    1. 去除 HTML 标签
    2. 格式化价格和销量
    3. 处理缺失值
    4. 去重检测
    """

    @staticmethod
    def clean_title(title: str) -> str:
        """清理商品标题"""
        if not title:
            return '未知商品'

        # 去除 HTML 标签
        import re
        title = re.sub(r'<[^>]+>', '', title)

        # 去除多余空白
        title = ' '.join(title.split())

        # 限制长度
        return title[:200]

    @staticmethod
    def clean_price(price: Any) -> Decimal:
        """
        清理价格字段

        Args:
            price: 原始价格（可能是字符串、数字等）

        Returns:
            Decimal: 标准化后的价格
        """
        if price is None:
            return Decimal('0.00')

        price_str = str(price)

        # 移除货币符号
        for symbol in ['¥', '￥', '$', '元', 'CNY']:
            price_str = price_str.replace(symbol, '')

        price_str = price_str.strip()

        try:
            return Decimal(str(price_str)).quantize(Decimal('0.01'))
        except (InvalidOperation, ValueError):
            logger.warning(f"价格转换失败: {price}")
            return Decimal('0.00')

    @staticmethod
    def clean_sales(sales: Any) -> int:
        """
        清理销量字段

        Args:
            sales: 原始销量（可能是字符串、数字等）

        Returns:
            int: 标准化后的销量
        """
        if sales is None:
            return 0

        sales_str = str(sales)

        # 移除常见修饰词
        for word in ['付款', '人付款', '+', '万', '千']:
            sales_str = sales_str.replace(word, ' ')

        # 处理万单位
        if '万' in str(sales):
            try:
                return int(float(str(sales).replace('万', '')) * 10000)
            except ValueError:
                pass

        try:
            return int(float(sales_str))
        except ValueError:
            return 0

    @staticmethod
    def clean_url(url: str) -> str:
        """清理 URL"""
        if not url:
            return ''

        url = url.strip()
        if not url.startswith('http'):
            return ''

        return url[:500]  # 限制长度

    @staticmethod
    def is_duplicate(product_data: Dict) -> bool:
        """
        检测商品是否重复

        Args:
            product_data: 商品数据

        Returns:
            bool: 是否重复
        """
        title = product_data.get('title', '')
        shop = product_data.get('shop', '')
        price = product_data.get('price')

        if not title:
            return False

        # 检查是否存在相同标题和店铺的商品
        queryset = Product.objects.filter(title=title, shop=shop)

        # 如果有价格，也检查价格是否接近
        if price:
            try:
                price_decimal = Decimal(str(price))
                queryset = queryset.filter(price__gte=price_decimal * Decimal('0.9'))
                queryset = queryset.filter(price__lte=price_decimal * Decimal('1.1'))
            except (InvalidOperation, ValueError):
                pass

        return queryset.exists()

    def process_item(self, item: Dict) -> Dict:
        """
        处理单个商品数据

        Args:
            item: 原始商品数据

        Returns:
            Dict: 清洗后的商品数据
        """
        return {
            'title': self.clean_title(item.get('title', '')),
            'price': self.clean_price(item.get('price')),
            'sales': self.clean_sales(item.get('sales')),
            'shop': str(item.get('shop', ''))[:100],
            'image_url': self.clean_url(item.get('image_url', '')),
            'detail_url': self.clean_url(item.get('detail_url', '')),
            'brand': str(item.get('brand', ''))[:50],
            'category': str(item.get('category', '宠物用品'))[:50],
        }


class BatchInsertPipeline:
    """
    批量插入管道

    功能：
    1. 积累数据到批次
    2. 批量写入数据库（优化性能）
    3. 错误处理和日志记录
    """

    def __init__(self, batch_size: int = 100):
        """
        初始化管道

        Args:
            batch_size: 批量写入大小
        """
        self.batch_size = batch_size
        self.buffer: List[Dict] = []
        self.saved_count = 0
        self.failed_count = 0
        self.batch_no = timezone.now().strftime('%Y%m%d%H%M%S')

    def add_item(self, item: Dict) -> bool:
        """
        添加商品到缓冲区

        Args:
            item: 商品数据

        Returns:
            bool: 是否添加成功
        """
        try:
            self.buffer.append(item)

            # 达到批量大小，执行插入
            if len(self.buffer) >= self.batch_size:
                self.flush()

            return True

        except Exception as e:
            logger.error(f"添加商品到缓冲区失败: {e}")
            self.failed_count += 1
            return False

    def flush(self):
        """将缓冲区数据批量写入数据库"""
        if not self.buffer:
            return

        try:
            products_to_create = []

            for item in self.buffer:
                try:
                    products_to_create.append(
                        Product(
                            title=item['title'],
                            price=item['price'],
                            sales=item['sales'],
                            shop=item['shop'],
                            image_url=item.get('image_url', ''),
                            detail_url=item.get('detail_url', ''),
                            brand=item.get('brand', ''),
                            category=item.get('category', '宠物用品'),
                            batch_no=self.batch_no,
                            crawl_time=timezone.now(),
                        )
                    )
                except Exception as e:
                    logger.error(f"准备商品数据失败: {e}")
                    self.failed_count += 1

            # 批量创建
            if products_to_create:
                Product.objects.bulk_create(products_to_create, batch_size=self.batch_size)
                self.saved_count += len(products_to_create)
                logger.info(f"批量插入成功: {len(products_to_create)} 条")

        except Exception as e:
            logger.error(f"批量插入失败: {e}")
            self.failed_count += len(self.buffer)

        finally:
            self.buffer.clear()

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'saved': self.saved_count,
            'failed': self.failed_count,
            'pending': len(self.buffer)
        }


class DataPipeline:
    """
    完整数据处理管道

    整合清洗和批量插入功能
    """

    def __init__(self, batch_size: int = 100):
        self.cleaning_pipeline = DataCleaningPipeline()
        self.batch_pipeline = BatchInsertPipeline(batch_size)

    def process(self, items: List[Dict]) -> Dict:
        """
        处理商品数据列表

        Args:
            items: 原始商品数据列表

        Returns:
            Dict: 处理结果统计
        """
        for item in items:
            # 检测重复
            if self.cleaning_pipeline.is_duplicate(item):
                logger.debug(f"跳过重复商品: {item.get('title')}")
                continue

            # 清洗数据
            cleaned = self.cleaning_pipeline.process_item(item)

            # 添加到批量缓冲区
            self.batch_pipeline.add_item(cleaned)

        # 刷新剩余数据
        self.batch_pipeline.flush()

        return self.batch_pipeline.get_stats()
