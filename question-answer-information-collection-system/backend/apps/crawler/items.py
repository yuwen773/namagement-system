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
    question_id = scrapy.Field()     # 问题ID（360问答原始ID）
    title = scrapy.Field()           # 问题标题
    source_url = scrapy.Field()      # 来源链接

    # 可选字段
    description = scrapy.Field()     # 问题描述
    category = scrapy.Field()        # 分类（如：影视、烦恼、软件）
    publish_time = scrapy.Field()    # 发布时间（格式：YYYY.MM.DD）
    location = scrapy.Field()        # 地理位置
    answer_count = scrapy.Field()    # 回答数量
    crawl_page = scrapy.Field()      # 爬取页码

    # 答案列表（多个答案）
    answer_list = scrapy.Field()     # 答案列表，每个元素是包含content、answerer、answer_time的字典

    # 元数据
    crawl_time = scrapy.Field()      # 采集时间

    def to_dict(self) -> dict:
        """
        转换为字典格式

        Returns:
            数据字典
        """
        return dict(self)


class AnswerItem(scrapy.Item):
    """
    答案数据 Item

    对应 crawler/models.py 中的 Answer 模型。
    """

    content = scrapy.Field()         # 答案内容
    answerer = scrapy.Field()        # 回答者
    answer_time = scrapy.Field()     # 回答时间
    source_order = scrapy.Field()    # 在源页面中的顺序


# 便捷函数：创建 QuestionItem
def create_question_item(
    question_id: str,
    title: str,
    source_url: str,
    description: str = None,
    category: str = None,
    publish_time: str = None,
    location: str = None,
    answer_count: int = 0,
    crawl_page: int = 1,
    answer_list: list = None
) -> QuestionItem:
    """
    创建 QuestionItem 的便捷函数

    Args:
        question_id: 问题ID（360问答原始ID）
        title: 问题标题
        source_url: 来源链接
        description: 问题描述
        category: 分类（如：影视、烦恼、软件）
        publish_time: 发布时间（格式：YYYY.MM.DD）
        location: 地理位置
        answer_count: 回答数量
        crawl_page: 爬取页码
        answer_list: 答案列表

    Returns:
        QuestionItem 实例
    """
    item = QuestionItem()

    item['question_id'] = question_id
    item['title'] = title
    item['source_url'] = source_url

    if description is not None:
        item['description'] = description

    if category is not None:
        item['category'] = category

    if publish_time is not None:
        item['publish_time'] = publish_time

    if location is not None:
        item['location'] = location

    if answer_count is not None:
        item['answer_count'] = answer_count

    if crawl_page is not None:
        item['crawl_page'] = crawl_page

    if answer_list is not None:
        item['answer_list'] = answer_list

    return item
