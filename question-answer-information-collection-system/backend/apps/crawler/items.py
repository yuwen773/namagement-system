"""
Scrapy Items 定义

定义爬虫要采集的数据结构。
"""

import scrapy
from itemadapter import ItemAdapter


class QuestionItem(scrapy.Item):
    """
    问答数据 Item

    对应 crawler/models.py 中的 Question 模型。
    """

    # 必填字段
    title = scrapy.Field()           # 问题标题
    answer_content = scrapy.Field()  # 回答内容
    source_url = scrapy.Field()      # 来源链接

    # 可选字段
    description = scrapy.Field()     # 问题描述
    answer_time = scrapy.Field()     # 回答时间
    answerer = scrapy.Field()         # 回答者
    tags = scrapy.Field()            # 标签列表

    # 元数据
    crawl_time = scrapy.Field()      # 采集时间

    def to_dict(self) -> dict:
        """
        转换为字典格式

        Returns:
            数据字典
        """
        return dict(self)


class TagItem(scrapy.Item):
    """
    标签数据 Item
    """

    name = scrapy.Field()


# 便捷函数：创建 QuestionItem
def create_question_item(
    title: str,
    answer_content: str,
    source_url: str,
    description: str = None,
    answer_time: str = None,
    answerer: str = None,
    tags: list = None
) -> QuestionItem:
    """
    创建 QuestionItem 的便捷函数

    Args:
        title: 问题标题
        answer_content: 回答内容
        source_url: 来源链接
        description: 问题描述
        answer_time: 回答时间
        answerer: 回答者
        tags: 标签列表

    Returns:
        QuestionItem 实例
    """
    item = QuestionItem()

    item['title'] = title
    item['answer_content'] = answer_content
    item['source_url'] = source_url

    if description is not None:
        item['description'] = description

    if answer_time is not None:
        item['answer_time'] = answer_time

    if answerer is not None:
        item['answerer'] = answerer

    if tags is not None:
        item['tags'] = tags

    return item
