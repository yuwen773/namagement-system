"""数据生成工具模块"""

import random
from datetime import timedelta
from faker import Faker

fake = Faker('zh_CN')

# 电影类型及权重
MOVIE_TYPES = [
    ('动作', 0.20),
    ('喜剧', 0.18),
    ('爱情', 0.15),
    ('科幻', 0.12),
    ('悬疑', 0.10),
    ('恐怖', 0.08),
    ('动画', 0.07),
    ('剧情', 0.05),
    ('战争', 0.03),
    ('惊悚', 0.02),
]

# 类型对应的片长范围（分钟）
TYPE_DURATION = {
    '动作': (90, 150),
    '喜剧': (80, 120),
    '爱情': (90, 130),
    '科幻': (100, 180),
    '悬疑': (90, 140),
    '恐怖': (75, 110),
    '动画': (70, 130),
    '剧情': (90, 150),
    '战争': (100, 180),
    '惊悚': (85, 120),
}

# 类型对应的票房范围（万元）
TYPE_BOXOFFICE = {
    '动作': (500, 50000),
    '喜剧': (300, 30000),
    '爱情': (200, 25000),
    '科幻': (1000, 80000),
    '悬疑': (300, 20000),
    '恐怖': (100, 15000),
    '动画': (500, 40000),
    '剧情': (100, 20000),
    '战争': (800, 60000),
    '惊悚': (200, 18000),
}

# 热门词汇
MOVIE_PREFIXES = ['超能', '星际', '传奇', '王者', '风暴', '联盟', '特工', '追凶', '末日', '重生',
                  '速度与激情', '流浪地球', '复仇者', '变形金刚', '蜘蛛侠', 'Batman', 'X战警',
                  '疯狂', '开心', '囧途', '大闹', '疯狂动物', '哪吒', '姜子牙', '熊出没']
MOVIE_WORDS = ['宇宙', '地球', '黎明', '黄昏', '之夜', '归来', '崛起', '终极', '决战', '起源',
              '行者', '飞驰', '狂潮', '烈焰', '冰霜', '雷霆', '风暴', '深海', '苍穹', '都市',
              '乡村', '校园', '职场', '商场', '战场', '沙场', '剧场', '赌场', '坟场', '刑场']
MOVIE_SUFFIXES = ['联盟', '宇宙', '传奇', '英雄', '崛起', '归来', '终结', '重生', '破晓', '逆袭',
                  '之恋', '之战', '之旅', '之路', '风云', '风暴', '狂欢', '谜案', '疑云', '真相']

# 导演/演员姓名库
DIRECTORS = ['张艺谋', '陈凯歌', '冯小刚', '姜文', '周星驰', '徐克', '吴京', '黄渤', '沈腾', '韩寒',
             '宁浩', '管虎', '陆川', '贾樟柯', '娄烨', '王小帅', '李安', '吴宇森', '周星驰', '王家卫',
             '克里斯托弗·诺兰', '詹姆斯·卡梅隆', '史蒂文·斯皮尔伯格', '马丁·斯科塞斯', '昆汀·塔伦蒂诺']
ACTORS = ['吴京', '沈腾', '黄渤', '徐峥', '邓超', '周星驰', '王宝强', '刘昊然', '易烊千玺', '王千源',
          '胡歌', '张译', '张涵予', '梁朝伟', '周润发', '成龙', '李连杰', '甄子丹', '赵又廷', '彭于晏',
          '马丽', '贾玲', '张小斐', '周冬雨', '刘亦菲', '杨幂', '赵丽颖', '杨紫', '迪丽热巴', 'Angelababy']


def generate_movie_title():
    """生成随机电影名称"""
    if random.random() < 0.3:
        # 英文+中文组合
        return f"{random.choice(MOVIE_PREFIXES)}: {fake.word().upper()}{random.choice(MOVIE_SUFFIXES)}"
    else:
        return f"{random.choice(MOVIE_PREFIXES)}{random.choice(MOVIE_WORDS)}{random.choice(MOVIE_SUFFIXES)}"


def select_movie_type():
    """根据权重选择电影类型"""
    types, weights = zip(*MOVIE_TYPES)
    return random.choices(types, weights=weights, k=1)[0]


def generate_movie_data(release_date):
    """生成单部电影的完整数据"""
    movie_type = select_movie_type()

    # 片长
    min_dur, max_dur = TYPE_DURATION.get(movie_type, (90, 120))
    duration = random.randint(min_dur, max_dur)

    # 票房（根据上映时间调整）
    min_bo, max_bo = TYPE_BOXOFFICE.get(movie_type, (100, 10000))
    # 周末/节假日上映的票房更高
    if release_date.weekday() in [4, 5, 6]:  # 周五周六周日
        min_bo *= 1.5
        max_bo *= 1.5
    # 暑期/贺岁档更高
    if release_date.month in [7, 8, 12, 1]:
        min_bo *= 1.3
        max_bo *= 1.3

    box_office_total = random.uniform(min_bo, max_bo)

    return {
        'title': generate_movie_title(),
        'director': random.choice(DIRECTORS) if random.random() > 0.3 else None,
        'actors': ', '.join(random.sample(ACTORS, random.randint(1, 5))),
        'release_date': release_date,
        'duration': duration,
        'type_name': movie_type,
        'box_office_total': round(box_office_total, 2),
    }


def get_release_dates(count, start_date, end_date):
    """生成均匀分布的上映日期"""
    delta = (end_date - start_date).days
    return [start_date + timedelta(days=random.randint(0, delta)) for _ in range(count)]


def decay_factor(day):
    """票房衰减系数（每周约15%衰减）"""
    return 0.85 ** (day / 7)
