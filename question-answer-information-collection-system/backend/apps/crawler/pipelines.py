"""
Scrapy Pipeline 模块

数据处理管道，负责：
1. 数据清洗
2. 重复检测
3. 批量入库
"""

import logging
from typing import Dict, Any, Optional
from itemadapter import ItemAdapter
from django.db import transaction
from django.utils import timezone

from .models import Question, Answer
from .utils import DataCleaner, DuplicateChecker

logger = logging.getLogger(__name__)


class QuestionPipeline:
    """
    问答数据处理管道

    集成 DataCleaner 进行数据清洗，使用 Django ORM 批量写入数据库。
    """

    # 批量插入的阈值
    BATCH_SIZE = 100

    def __init__(self):
        """初始化管道"""
        self.cleaner = DataCleaner()
        self.duplicate_checker = DuplicateChecker()
        self.items_buffer: list = []
        self.stats = {
            'processed': 0,
            'cleaned': 0,
            'duplicates': 0,
            'errors': 0,
            'inserted': 0,
        }

    def open_spider(self, spider):
        """
        爬虫启动时调用

        Args:
            spider: 爬虫实例
        """
        logger.info("QuestionPipeline 启动")
        self.duplicate_checker.reset()
        self.items_buffer.clear()
        self._reset_stats()

    def close_spider(self, spider):
        """
        爬虫关闭时调用

        Args:
            spider: 爬虫实例
        """
        logger.info("QuestionPipeline 关闭")
        # 确保缓冲数据入库
        self._flush_buffer()
        self._log_stats()

    def _reset_stats(self):
        """重置统计信息"""
        self.stats = {
            'processed': 0,
            'cleaned': 0,
            'duplicates': 0,
            'errors': 0,
            'inserted': 0,
        }

    def _log_stats(self):
        """记录统计信息"""
        logger.info(
            f"Pipeline 统计: 处理 {self.stats['processed']} 条, "
            f"清洗 {self.stats['cleaned']} 条, "
            f"重复 {self.stats['duplicates']} 条, "
            f"入库 {self.stats['inserted']} 条, "
            f"错误 {self.stats['errors']} 条"
        )

    def process_item(self, item: Dict[str, Any], spider) -> Dict[str, Any]:
        """
        处理单个数据项

        Args:
            item: Scrapy Item 或字典
            spider: 爬虫实例

        Returns:
            处理后的 item
        """
        try:
            self.stats['processed'] += 1

            # 转换为字典
            data = ItemAdapter(item).asdict()

            # 数据清洗
            cleaned_data = self.cleaner.clean_item(data)
            self.stats['cleaned'] += 1

            # 验证数据
            is_valid, errors = self.cleaner.validate_data(cleaned_data)
            if not is_valid:
                logger.warning(f"数据验证失败: {errors}")
                self.stats['errors'] += 1
                return item

            # 检查重复
            title = cleaned_data.get('title', '')
            source_url = cleaned_data.get('source_url', '')

            if self.duplicate_checker.is_duplicate(title, source_url):
                logger.debug(f"重复数据，跳过: {title[:50]}...")
                self.stats['duplicates'] += 1
                return item

            # 添加到缓冲池
            self.items_buffer.append(cleaned_data)

            # 批量入库
            if len(self.items_buffer) >= self.BATCH_SIZE:
                self._flush_buffer()

        except Exception as e:
            logger.error(f"处理 item 失败: {e}")
            self.stats['errors'] += 1

        return item

    def _flush_buffer(self):
        """
        将缓冲池中的数据批量写入数据库
        """
        if not self.items_buffer:
            return

        try:
            inserted = self._batch_insert(self.items_buffer)
            self.stats['inserted'] += inserted
            self.items_buffer.clear()
            logger.info(f"批量入库 {inserted} 条数据")
        except Exception as e:
            logger.error(f"批量入库失败: {e}")
            self.stats['errors'] += len(self.items_buffer)
            self.items_buffer.clear()

    def _batch_insert(self, items: list) -> int:
        """
        批量插入数据

        Args:
            items: 数据字典列表

        Returns:
            成功插入的数量
        """
        if not items:
            return 0

        inserted_count = 0

        # 使用 Django 事务确保数据一致性
        with transaction.atomic():
            for item_data in items:
                try:
                    # 检查是否已存在（双重保险）
                    if Question.objects.filter(
                        source_url=item_data['source_url']
                    ).exists():
                        self.stats['duplicates'] += 1
                        continue

                    # 创建 Question 实例
                    question = Question(
                        question_id=item_data.get('question_id', ''),
                        title=item_data.get('title', ''),
                        description=item_data.get('description'),
                        category=item_data.get('category'),
                        publish_time=item_data.get('publish_time'),
                        location=item_data.get('location'),
                        answer_count=item_data.get('answer_count', 0),
                        crawl_page=item_data.get('crawl_page', 1),
                        source_url=item_data['source_url'],
                    )
                    question.save()

                    # 处理答案列表（如果有多个答案）
                    answer_list = item_data.get('answer_list', [])
                    if answer_list:
                        self._handle_answers(question, answer_list)

                    inserted_count += 1

                except Exception as e:
                    logger.error(f"插入单条数据失败: {e}")
                    self.stats['errors'] += 1

        return inserted_count

    def _handle_answers(self, question: Question, answer_list: list):
        """
        处理答案关联

        Args:
            question: Question 实例
            answer_list: 答案数据列表
        """
        if not isinstance(answer_list, list):
            return

        for idx, answer_data in enumerate(answer_list, start=1):
            if not isinstance(answer_data, dict):
                continue

            try:
                Answer.objects.create(
                    question=question,
                    content=answer_data.get('content', ''),
                    answerer=answer_data.get('answerer'),
                    answer_time=answer_data.get('answer_time'),
                    source_order=idx,
                )
            except Exception as e:
                logger.error(f"插入答案失败: {e}")


    def get_stats(self) -> Dict[str, int]:
        """
        获取管道统计信息

        Returns:
            统计字典
        """
        return self.stats.copy()


class DuplicateFilterPipeline:
    """
    重复过滤管道（简化版）

    仅负责去重，不处理入库逻辑。
    适用于需要与其他 Pipeline 配合的场景。
    """

    def __init__(self):
        self.duplicate_checker = DuplicateChecker()

    def open_spider(self, spider):
        """爬虫启动"""
        self.duplicate_checker.reset()

    def process_item(self, item: Dict[str, Any], spider) -> Optional[Dict[str, Any]]:
        """
        处理 item，返回 None 表示丢弃

        Args:
            item: 数据项
            spider: 爬虫实例

        Returns:
            处理后的 item 或 None
        """
        title = item.get('title', '')
        source_url = item.get('source_url', '')

        if self.duplicate_checker.is_duplicate(title, source_url):
            logger.debug(f"重复数据，跳过: {title[:50]}...")
            return None

        return item


class DataValidationPipeline:
    """
    数据验证管道

    验证数据完整性和格式，不符合要求的数据会被丢弃。
    """

    REQUIRED_FIELDS = ['question_id', 'title', 'source_url']

    def process_item(self, item: Dict[str, Any], spider) -> Optional[Dict[str, Any]]:
        """
        验证 item，必填字段缺失则丢弃

        Args:
            item: 数据项
            spider: 爬虫实例

        Returns:
            验证通过的 item 或 None
        """
        for field in self.REQUIRED_FIELDS:
            value = item.get(field)
            if not value or (isinstance(value, str) and not value.strip()):
                logger.warning(f"必填字段 {field} 缺失，跳过")
                return None

        return item
