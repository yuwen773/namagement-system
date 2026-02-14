"""
景点数据清洗模块
用于处理和清洗从 Excel 文件导入的景点数据
"""

import pandas as pd
import re


class AttractionDataCleaner:
    """景点数据清洗器"""

    # 地名到类别的映射
    CATEGORY_BY_CITY = {
        # 人文古迹类城市
        '北京': '人文古迹', '西安': '人文古迹', '南京': '人文古迹',
        '洛阳': '人文古迹', '杭州': '人文古迹', '苏州': '人文古迹',
        '平遥': '人文古迹', '承德': '人文古迹', '拉萨': '人文古迹',
        '开封': '人文古迹', '安阳': '人文古迹', '大同': '人文古迹',
        '沈阳': '人文古迹', '武汉': '人文古迹', '荆州': '人文古迹',
        '南昌': '人文古迹', '成都': '人文古迹', '遵义': '人文古迹',
        '大理': '人文古迹', '丽江': '人文古迹', '大理白族自治州': '人文古迹',
        '阆中': '人文古迹', '徐州': '人文古迹', '镇江': '人文古迹',
        '宁波': '人文古迹', '绍兴': '人文古迹', '嘉兴': '人文古迹',
        '泉州': '人文古迹', '福州': '人文古迹', '广州': '人文古迹',
        '潮州': '人文古迹', '佛山': '人文古迹', '开封': '人文古迹',
        '郑州': '人文古迹', '南阳': '人文古迹', '襄阳': '人文古迹',
        '宜宾': '人文古迹', '大理': '人文古迹',

        # 自然风光类城市
        '张家界': '自然风光', '桂林': '自然风光', '九寨沟': '自然风光',
        '黄山': '自然风光', '三亚': '自然风光', '厦门': '自然风光',
        '青岛': '自然风光', '大连': '自然风光', '烟台': '自然风光',
        '威海': '自然风光', '秦皇岛': '自然风光', '海口': '自然风光',
        '西宁': '自然风光', '兰州': '自然风光', '乌鲁木齐': '自然风光',
        '拉萨': '自然风光', '昆明': '自然风光', '贵阳': '自然风光',
        '长沙': '自然风光', '吉林': '自然风光', '长春': '自然风光',
        '哈尔滨': '自然风光', '牡丹江': '自然风光', '延边': '自然风光',
        '清远': '自然风光', '韶关': '自然风光', '肇庆': '自然风光',
        '阳朔': '自然风光', '北海': '自然风光', '柳州': '自然风光',
        '梧州': '自然风光', '贺州': '自然风光', '池州': '自然风光',
        '安庆': '自然风光', '黄山市': '自然风光', '丽水': '自然风光',
        '舟山': '自然风光', '台州': '自然风光', '衢州': '自然风光',
        '金华': '自然风光', '湖州': '自然风光', '南通': '自然风光',
        '连云港': '自然风光', '日照': '自然风光', '潍坊': '自然风光',
        '滨州': '自然风光', '三亚': '自然风光',

        # 主题乐园类城市
        '上海': '主题乐园', '广州': '主题乐园', '深圳': '主题乐园',
        '天津': '主题乐园', '重庆': '主题乐园', '成都': '主题乐园',
        '武汉': '主题乐园', '南京': '主题乐园', '苏州': '主题乐园',
    }

    # 景点名关键词分类
    CATEGORY_KEYWORDS = {
        '人文古迹': ['寺', '庙', '宫', '陵', '墓', '长城', '故宫', '兵马俑', '塔', '楼', '阁', '院', '窟', '观', '祠', '亭', '桥', '古', '城', '遗址', '石窟', '碑林', '文庙', '孔庙'],
        '自然风光': ['山', '湖', '江', '河', '海', '瀑布', '森林', '公园', '岛', '泉', '峡', '谷', '峰', '林', '草', '原', '湿地', '竹', '溪', '潭', '池', '瀑', '沙', '滩'],
        '主题乐园': ['迪士尼', '乐园', '欢乐谷', '方特', '海洋公园', '水族馆', '动物园', '游乐场', '度假区', '欢乐世界', '长隆', '万达'],
        '现代建筑': ['塔', '桥', '广场', '中心', '大厦', '会展', '博览', '科技馆', '博物馆', '展览馆', '图书馆', '大剧院', '音乐厅', '体育', '会展'],
    }

    @classmethod
    def clean_rating(cls, rating_str):
        """清洗星级：'94%' -> 0.94 或 94.0"""
        if pd.isna(rating_str):
            return 0.0
        try:
            # 移除百分号并转换为浮点数
            value = str(rating_str).replace('%', '').strip()
            return float(value) if value else 0.0
        except (ValueError, TypeError):
            return 0.0

    @classmethod
    def clean_coordinate(cls, value):
        """清洗坐标值"""
        if pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @classmethod
    def clean_integer(cls, value):
        """清洗整数值"""
        if pd.isna(value):
            return 0
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return 0

    @classmethod
    def clean_text(cls, value):
        """清洗文本值"""
        if pd.isna(value):
            return ''
        return str(value).strip()

    @classmethod
    def infer_category(cls, city, name):
        """推断景点类别"""
        city = city or ''
        name = name or ''

        # 先按城市推断
        if city in cls.CATEGORY_BY_CITY:
            return cls.CATEGORY_BY_CITY[city]

        # 再按景点名关键词推断
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in name:
                    return category

        return '其他'

    @classmethod
    def clean_dataset2(cls, df):
        """
        清洗数据集2 - 全国旅游景点及描述.xls

        字段映射：
        - 景点名 -> name
        - 简介 -> description
        - 地名 + 景点名 -> address
        - 地名 -> region
        - 评论人数 -> view_count
        - 攻略数量 -> guide_count
        - 排名 -> ranking
        - 星级 -> rating_percentage
        - 经度 -> longitude
        - 纬度 -> latitude
        """
        cleaned = pd.DataFrame()

        # 基本字段映射
        cleaned['name'] = df['景点名'].apply(cls.clean_text)
        cleaned['description'] = df['简介'].apply(cls.clean_text)
        cleaned['region'] = df['地名'].apply(cls.clean_text)
        cleaned['view_count'] = df['评论人数'].apply(cls.clean_integer)
        cleaned['guide_count'] = df['攻略数量'].apply(cls.clean_integer)
        cleaned['ranking'] = df['排名'].apply(cls.clean_integer)
        cleaned['rating_percentage'] = df['星级'].apply(cls.clean_rating)
        cleaned['longitude'] = df['经度'].apply(cls.clean_coordinate)
        cleaned['latitude'] = df['纬度'].apply(cls.clean_coordinate)

        # 组合地址
        cleaned['address'] = df.apply(
            lambda row: f"{row['地名']} {row['景点名']}".strip() if pd.notna(row['地名']) else row['景点名'],
            axis=1
        )

        # 推断类别
        cleaned['category'] = df.apply(
            lambda row: cls.infer_category(row['地名'], row['景点名']),
            axis=1
        )

        # 默认值 - 使用与 DataFrame 相同长度
        cleaned['opening_hours'] = '全天开放'
        cleaned['images'] = [[] for _ in range(len(df))]
        cleaned['cover_image'] = ''
        cleaned['level'] = ''

        return cleaned.reset_index(drop=True)

    @classmethod
    def clean_dataset1(cls, df):
        """
        清洗数据集1 - 全国5A级景区.xlsx

        字段映射：
        - dth_title -> name
        - Province -> region
        - time -> 评定年份（可存储在额外字段或忽略）
        - bd_lon/gg_lon -> longitude
        - bd_lat/gg_lat -> latitude
        - level -> level (5A)
        """
        cleaned = pd.DataFrame()

        # 基本字段映射
        cleaned['name'] = df['dth_title'].apply(cls.clean_text)
        cleaned['region'] = df['Province'].apply(cls.clean_text)
        cleaned['level'] = '5A'

        # 坐标优先使用百度坐标，其次是高德坐标
        cleaned['longitude'] = df.apply(
            lambda row: row['bd_lon'] if pd.notna(row.get('bd_lon')) else row.get('gg_lon'),
            axis=1
        )
        cleaned['latitude'] = df.apply(
            lambda row: row['bd_lat'] if pd.notna(row.get('bd_lat')) else row.get('gg_lat'),
            axis=1
        )

        # 清洗坐标
        cleaned['longitude'] = cleaned['longitude'].apply(cls.clean_coordinate)
        cleaned['latitude'] = cleaned['latitude'].apply(cls.clean_coordinate)

        # 其他字段使用默认值
        cleaned['description'] = ''
        cleaned['address'] = df.apply(
            lambda row: f"{row['Province']} {row['dth_title']}".strip() if pd.notna(row.get('Province')) else row['dth_title'],
            axis=1
        )
        cleaned['category'] = '其他'  # 5A级景区不自动分类，保留为其他
        cleaned['opening_hours'] = '全天开放'
        cleaned['images'] = [[] for _ in range(len(df))]
        cleaned['cover_image'] = ''
        cleaned['view_count'] = 0
        cleaned['guide_count'] = 0
        cleaned['ranking'] = None
        cleaned['rating_percentage'] = 0.0

        return cleaned.reset_index(drop=True)

    @classmethod
    def remove_duplicates(cls, df, keep='first'):
        """去除重复记录"""
        # 按名称去重
        if 'name' in df.columns:
            before = len(df)
            df = df.drop_duplicates(subset=['name'], keep=keep)
            after = len(df)
            return df, before - after
        return df, 0

    @classmethod
    def validate_records(cls, df):
        """验证记录的有效性"""
        issues = {
            'empty_name': 0,
            'empty_description': 0,
            'invalid_coordinates': 0,
        }

        for idx, row in df.iterrows():
            if not row.get('name'):
                issues['empty_name'] += 1
            if not row.get('description'):
                issues['empty_description'] += 1
            # 验证坐标范围（中国区域大致范围）
            lat = row.get('latitude')
            lon = row.get('longitude')
            if lat is not None and (lat < 18 or lat > 54):
                issues['invalid_coordinates'] += 1
            if lon is not None and (lon < 73 or lon < 135):
                issues['invalid_coordinates'] += 1

        return issues
