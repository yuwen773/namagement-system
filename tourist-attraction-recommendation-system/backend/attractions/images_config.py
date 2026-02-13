"""
景点图片 URL 配置文件

使用 Unsplash 公开图片源，为景点提供高质量的封面图和轮播图。
图片 URL 格式说明:
- cover: 800px 宽度封面图
- gallery: 1200px 宽度轮播图 (3-4张)

所有图片均来自 Unsplash 公开资源，符合使用条款。
"""

# 景点图片配置 - 使用确实有效的 Unsplash 图片
# 格式: { "景点名称": { "pinyin": "拼音", "cover": "封面图URL", "gallery": [轮播图列表] } }
ATTRACTION_IMAGES = {
    "故宫": {
        "pinyin": "gugong",
        "cover": "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=1200&q=80",
            "https://images.unsplash.com/photo-1599658880436-c61792e70672?w=1200&q=80",
            "https://images.unsplash.com/photo-1529686734068-64bdda8ad66c?w=1200&q=80",
            "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
        ],
    },
    "长城": {
        "pinyin": "changcheng",
        "cover": "https://images.unsplash.com/photo-1537895593488-eb03e607c7fa?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1537895593488-eb03e607c7fa?w=1200&q=80",
            "https://images.unsplash.com/photo-1551524559-8af4e6624178?w=1200&q=80",
            "https://images.unsplash.com/photo-1564415315949-7a0c4c73aab4?w=1200&q=80",
            "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
        ],
    },
    "西湖": {
        "pinyin": "xihu",
        "cover": "https://images.unsplash.com/photo-1597326228591-6c4c82644d41?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1597326228591-6c4c82644d41?w=1200&q=80",
            "https://images.unsplash.com/photo-1597326556228-468c324d18dc?w=1200&q=80",
            "https://images.unsplash.com/photo-1679683363530-41b2b6698509?w=1200&q=80",
            "https://images.unsplash.com/photo-1537531383496-f4749a4b8590?w=1200&q=80",
        ],
    },
    "黄山": {
        "pinyin": "huangshan",
        "cover": "https://images.unsplash.com/photo-1604840675593-210c06b444d5?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1604840675593-210c06b444d5?w=1200&q=80",
            "https://images.unsplash.com/photo-1624821562767-0b1e0f581143?w=1200&q=80",
            "https://images.unsplash.com/photo-1602218705798-87e4d29cc3c2?w=1200&q=80",
            "https://images.unsplash.com/photo-1597926660694-1a5927b660e4?w=1200&q=80",
        ],
    },
    "九寨沟": {
        "pinyin": "jiuzhaigou",
        "cover": "https://images.unsplash.com/photo-1587578932405-7c740a762f3e?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1587578932405-7c740a762f3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1565025997446-f86f1f658ade?w=1200&q=80",
            "https://images.unsplash.com/photo-1568691468714-f375135c2b64?w=1200&q=80",
            "https://images.unsplash.com/photo-1565025997446-f86f1f658ade?w=1200&q=80",
        ],
    },
    "鼓浪屿": {
        "pinyin": "gulangyu",
        "cover": "https://images.unsplash.com/photo-1562690868-60bbe7621e3c?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1562690868-60bbe7621e3c?w=1200&q=80",
            "https://images.unsplash.com/photo-1562792675-69df99300028?w=1200&q=80",
            "https://images.unsplash.com/photo-1562690868-60bbe7621e3c?w=1200&q=80",
            "https://images.unsplash.com/photo-1562792675-69df99300028?w=1200&q=80",
        ],
    },
    "上海迪士尼乐园": {
        "pinyin": "shanghai_disney",
        "cover": "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=1200&q=80",
            "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&q=80",
            "https://images.unsplash.com/photo-1533114876105-5fe5019509d8?w=1200&q=80",
            "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=1200&q=80",
        ],
    },
    "张家界国家森林公园": {
        "pinyin": "zhangjiajie",
        "cover": "https://images.unsplash.com/photo-1587578932405-7c740a762f3e?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1587578932405-7c740a762f3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1565025997446-f86f1f658ade?w=1200&q=80",
            "https://images.unsplash.com/photo-1568691468714-f375135c2b64?w=1200&q=80",
            "https://images.unsplash.com/photo-1565025997446-f86f1f658ade?w=1200&q=80",
        ],
    },
    "兵马俑": {
        "pinyin": "bingmayong",
        "cover": "https://images.unsplash.com/photo-1597926660694-1a5927b660e4?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1597926660694-1a5927b660e4?w=1200&q=80",
            "https://images.unsplash.com/photo-1604840675593-210c06b444d5?w=1200&q=80",
            "https://images.unsplash.com/photo-1624821562767-0b1e0f581143?w=1200&q=80",
            "https://images.unsplash.com/photo-1602218705798-87e4d29cc3c2?w=1200&q=80",
        ],
    },
    "桂林山水": {
        "pinyin": "guilinshanshui",
        "cover": "https://images.unsplash.com/photo-1537531383496-f4749a4b8590?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1537531383496-f4749a4b8590?w=1200&q=80",
            "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=1200&q=80",
            "https://images.unsplash.com/photo-1599658880436-c61792e70672?w=1200&q=80",
            "https://images.unsplash.com/photo-1529686734068-64bdda8ad66c?w=1200&q=80",
        ],
    },
    "丽江古城": {
        "pinyin": "lijiang",
        "cover": "https://images.unsplash.com/photo-1562690868-60bbe7621e3c?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1562690868-60bbe7621e3c?w=1200&q=80",
            "https://images.unsplash.com/photo-1562792675-69df99300028?w=1200&q=80",
            "https://images.unsplash.com/photo-1562690868-60bbe7621e3c?w=1200&q=80",
            "https://images.unsplash.com/photo-1562792675-69df99300028?w=1200&q=80",
        ],
    },
    "三亚湾": {
        "pinyin": "sanyawan",
        "cover": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1200&q=80",
            "https://images.unsplash.com/photo-1506953823976-52e1fdc0149a?w=1200&q=80",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80",
        ],
    },
}

# 类别默认图片配置 - 使用确实有效的 Unsplash 图片
CATEGORY_DEFAULT_IMAGES = {
    "自然风光": {
        "cover": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200&q=80",
            "https://images.unsplash.com/photo-1518173946687-a4c036bc1e3e?w=1200&q=80",
        ],
    },
    "人文古迹": {
        "cover": "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?w=1200&q=80",
            "https://images.unsplash.com/photo-1599658880436-c61792e70672?w=1200&q=80",
            "https://images.unsplash.com/photo-1529686734068-64bdda8ad66c?w=1200&q=80",
            "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1200&q=80",
        ],
    },
    "主题乐园": {
        "cover": "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=1200&q=80",
            "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&q=80",
            "https://images.unsplash.com/photo-1533114876105-5fe5019509d8?w=1200&q=80",
            "https://images.unsplash.com/photo-1559671459-5b3cb6048429?w=1200&q=80",
        ],
    },
    "海滩": {
        "cover": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1200&q=80",
            "https://images.unsplash.com/photo-1506953823976-52e1fdc0149a?w=1200&q=80",
            "https://images.unsplash.com/photo-1518173946687-a4c036bc1e3e?w=1200&q=80",
        ],
    },
    "其他": {
        "cover": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&q=80",
            "https://images.unsplash.com/photo-1518173946687-a4c036bc1e3e?w=1200&q=80",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1200&q=80",
        ],
    },
}


def get_attraction_image(attraction_name: str, image_type: str = "cover") -> str | None:
    """
    获取景点图片 URL

    Args:
        attraction_name: 景点名称
        image_type: 图片类型 ("cover" 或 "gallery")

    Returns:
        图片 URL 字符串，如果是 gallery 则返回第一张图
    """
    if attraction_name not in ATTRACTION_IMAGES:
        return None

    if image_type == "cover":
        return ATTRACTION_IMAGES[attraction_name].get("cover")
    elif image_type == "gallery":
        gallery = ATTRACTION_IMAGES[attraction_name].get("gallery", [])
        return gallery[0] if gallery else None

    return None


def get_attraction_gallery(attraction_name: str) -> list:
    """
    获取景点轮播图列表

    Args:
        attraction_name: 景点名称

    Returns:
        轮播图 URL 列表
    """
    if attraction_name not in ATTRACTION_IMAGES:
        return []

    return ATTRACTION_IMAGES[attraction_name].get("gallery", [])


def get_all_attraction_images() -> dict:
    """
    获取所有景点图片配置

    Returns:
        所有景点图片配置的字典
    """
    return ATTRACTION_IMAGES


def get_category_default_images(category: str) -> dict:
    """
    获取类别默认图片

    Args:
        category: 景点类别

    Returns:
        包含 cover 和 gallery 的字典
    """
    # 处理类别名称映射
    category_map = {
        "自然风光": "自然风光",
        "人文古迹": "人文古迹",
        "主题乐园": "主题乐园",
        "海滩": "海滩",
        "海滩/海滨": "海滩",
        "其他": "其他",
    }
    mapped = category_map.get(category, "其他")
    return CATEGORY_DEFAULT_IMAGES.get(mapped, CATEGORY_DEFAULT_IMAGES["其他"])
