"""
Django management command to seed initial data for the tourist attraction system.

Usage:
    python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from accounts.models import UserProfile
from attractions.models import Attraction
from comments.models import Comment, Favorite
from notifications.models import Notification


class Command(BaseCommand):
    help = 'Seed initial data for the tourist attraction system'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')

        # 1. 创建管理员账号
        self.stdout.write('创建管理员账号...')
        admin_data = [
            {
                'username': 'admin',
                'password': 'admin123',
                'real_name': '系统管理员',
                'phone': '13800000000',
                'email': 'admin@example.com',
                'role': 'ADMIN',
            },
        ]
        for data in admin_data:
            user, created = UserProfile.objects.get_or_create(
                username=data['username'],
                defaults={
                    'password': data['password'],  # Django会自动hash
                    'real_name': data['real_name'],
                    'phone': data['phone'],
                    'email': data['email'],
                    'role': data['role'],
                }
            )
            if created:
                self.stdout.write(f'  - 创建管理员: {data["username"]}')
            else:
                self.stdout.write(f'  - 管理员已存在: {data["username"]}')

        # 2. 创建测试用户账号
        self.stdout.write('创建测试用户账号...')
        user_data = [
            {
                'username': 'user',
                'password': 'user123',
                'real_name': '测试用户',
                'phone': '13800000001',
                'email': 'user@example.com',
                'role': 'USER',
            },
            {
                'username': 'test1',
                'password': 'test123',
                'real_name': '测试用户1',
                'phone': '13800000002',
                'email': 'test1@example.com',
                'role': 'USER',
            },
            {
                'username': 'test2',
                'password': 'test123',
                'real_name': '测试用户2',
                'phone': '13800000003',
                'email': 'test2@example.com',
                'role': 'USER',
            },
        ]
        for data in user_data:
            user, created = UserProfile.objects.get_or_create(
                username=data['username'],
                defaults={
                    'password': data['password'],
                    'real_name': data['real_name'],
                    'phone': data['phone'],
                    'email': data['email'],
                    'role': data['role'],
                }
            )
            if created:
                self.stdout.write(f'  - 创建用户: {data["username"]}')
            else:
                self.stdout.write(f'  - 用户已存在: {data["username"]}')

        # 3. 创建示例景点数据
        self.stdout.write('创建示例景点数据...')
        attraction_data = [
            {
                'name': '故宫',
                'description': '中国明清两代的皇家宫殿，世界上最大的古代宫殿之一',
                'address': '北京市东城区景山前街4号',
                'category': '人文古迹',
                'region': '华北',
                'opening_hours': '8:30-17:00',
                'cover_image': 'gugong.jpg',
                'images': ['gugong_1.jpg', 'gugong_2.jpg', 'gugong_3.jpg'],
                'view_count': 1500,
            },
            {
                'name': '长城',
                'description': '世界文化遗产，世界上最著名的古代防御工程',
                'address': '北京市延庆区G6京藏高速58号出口',
                'category': '人文古迹',
                'region': '华北',
                'opening_hours': '7:00-18:00',
                'cover_image': 'changcheng.jpg',
                'images': ['changcheng_1.jpg', 'changcheng_2.jpg'],
                'view_count': 2000,
            },
            {
                'name': '西湖',
                'description': '中国首批国家重点风景名胜区和国家5A级旅游景区',
                'address': '浙江省杭州市西湖区',
                'category': '自然风光',
                'region': '华东',
                'opening_hours': '全天开放',
                'cover_image': 'xihu.jpg',
                'images': ['xihu_1.jpg', 'xihu_2.jpg', 'xihu_3.jpg'],
                'view_count': 1800,
            },
            {
                'name': '黄山',
                'description': '五岳归来不看山，黄山归来不看岳',
                'address': '安徽省黄山市黄山区',
                'category': '自然风光',
                'region': '华东',
                'opening_hours': '6:00-17:30',
                'cover_image': 'huangshan.jpg',
                'images': ['huangshan_1.jpg', 'huangshan_2.jpg'],
                'view_count': 1200,
            },
            {
                'name': '九寨沟',
                'description': '童话世界，天然翡翠',
                'address': '四川省阿坝藏族羌族自治州九寨沟县',
                'category': '自然风光',
                'region': '西南',
                'opening_hours': '7:00-18:00',
                'cover_image': 'jiuzhaigou.jpg',
                'images': ['jiuzhaigou_1.jpg', 'jiuzhaigou_2.jpg'],
                'view_count': 1100,
            },
            {
                'name': '鼓浪屿',
                'description': '万国建筑博览，音乐之岛',
                'address': '福建省厦门市思明区',
                'category': '人文古迹',
                'region': '华东',
                'opening_hours': '全天开放',
                'cover_image': 'gulangyu.jpg',
                'images': ['gulangyu_1.jpg', 'gulangyu_2.jpg'],
                'view_count': 900,
            },
            {
                'name': '上海迪士尼乐园',
                'description': '中国内地首座迪士尼主题乐园',
                'address': '上海市浦东新区川沙新镇',
                'category': '主题乐园',
                'region': '华东',
                'opening_hours': '9:00-21:00',
                'cover_image': 'disney.jpg',
                'images': ['disney_1.jpg', 'disney_2.jpg', 'disney_3.jpg'],
                'view_count': 2500,
            },
            {
                'name': '张家界国家森林公园',
                'description': '世界自然遗产，世界地质公园',
                'address': '湖南省张家界市武陵源区',
                'category': '自然风光',
                'region': '华中',
                'opening_hours': '7:00-18:00',
                'cover_image': 'zhangjiajie.jpg',
                'images': ['zhangjiajie_1.jpg', 'zhangjiajie_2.jpg'],
                'view_count': 1300,
            },
            {
                'name': '兵马俑',
                'description': '世界第八大奇迹',
                'address': '陕西省西安市临潼区秦陵北路',
                'category': '人文古迹',
                'region': '西北',
                'opening_hours': '8:30-18:00',
                'cover_image': 'bengmanyong.jpg',
                'images': ['bengmanyong_1.jpg', 'bengmanyong_2.jpg'],
                'view_count': 1600,
            },
            {
                'name': '桂林山水',
                'description': '桂林山水甲天下',
                'address': '广西壮族自治区桂林市',
                'category': '自然风光',
                'region': '华南',
                'opening_hours': '全天开放',
                'cover_image': 'guilin.jpg',
                'images': ['guilin_1.jpg', 'guilin_2.jpg'],
                'view_count': 1400,
            },
            {
                'name': '丽江古城',
                'description': '世界文化遗产，纳西族文化的活化石',
                'address': '云南省丽江市古城区',
                'category': '人文古迹',
                'region': '西南',
                'opening_hours': '全天开放',
                'cover_image': 'lijiang.jpg',
                'images': ['lijiang_1.jpg', 'lijiang_2.jpg'],
                'view_count': 1000,
            },
            {
                'name': '三亚湾',
                'description': '热带海滨风光度假胜地',
                'address': '海南省三亚市三亚湾路',
                'category': '自然风光',
                'region': '华南',
                'opening_hours': '全天开放',
                'cover_image': 'sanyawan.jpg',
                'images': ['sanyawan_1.jpg', 'sanyawan_2.jpg'],
                'view_count': 1700,
            },
        ]

        for data in attraction_data:
            attraction, created = Attraction.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  - 创建景点: {data["name"]}')
            else:
                self.stdout.write(f'  - 景点已存在: {data["name"]}')

        # 4. 创建示例评论
        self.stdout.write('创建示例评论...')
        admin_user = UserProfile.objects.filter(username='admin').first()
        user1 = UserProfile.objects.filter(username='user').first()
        user2 = UserProfile.objects.filter(username='test1').first()
        user3 = UserProfile.objects.filter(username='test2').first()

        comment_data = [
            {'user': user1, 'attraction': Attraction.objects.get(name='故宫'), 'content': '非常壮观的皇家宫殿，建筑宏伟，值得一游！', 'rating': 5, 'status': 'APPROVED'},
            {'user': user1, 'attraction': Attraction.objects.get(name='长城'), 'content': '长城真的很壮观，体力消耗较大，建议穿舒适的鞋子', 'rating': 5, 'status': 'APPROVED'},
            {'user': user2, 'attraction': Attraction.objects.get(name='西湖'), 'content': '西湖美景如画，苏堤春晓令人难忘', 'rating': 5, 'status': 'APPROVED'},
            {'user': user2, 'attraction': Attraction.objects.get(name='九寨沟'), 'content': '九寨沟的水色彩斑斓，宛如童话世界', 'rating': 5, 'status': 'APPROVED'},
            {'user': user3, 'attraction': Attraction.objects.get(name='上海迪士尼乐园'), 'content': '迪士尼乐园氛围很好，项目都很精彩', 'rating': 4, 'status': 'APPROVED'},
            {'user': user1, 'attraction': Attraction.objects.get(name='兵马俑'), 'content': '兵马俑的震撼无法用语言形容，历史的厚重感', 'rating': 5, 'status': 'PENDING'},
            {'user': user2, 'attraction': Attraction.objects.get(name='张家界国家森林公园'), 'content': '张家界的峰林地貌独特，壮观极了', 'rating': 5, 'status': 'APPROVED'},
            {'user': user3, 'attraction': Attraction.objects.get(name='黄山'), 'content': '黄山日出、云海、奇松、怪石，美不胜收', 'rating': 5, 'status': 'APPROVED'},
        ]

        for data in comment_data:
            if data['user'] and data['attraction']:
                comment, created = Comment.objects.get_or_create(
                    user=data['user'],
                    attraction=data['attraction'],
                    content=data['content'],
                    defaults={
                        'rating': data['rating'],
                        'status': data['status'],
                    }
                )
                if created:
                    self.stdout.write(f'  - 创建评论: {data["user"].username}@{data["attraction"].name}')

        # 5. 创建示例收藏
        self.stdout.write('创建示例收藏...')
        favorite_data = [
            {'user': user1, 'attraction': Attraction.objects.get(name='故宫')},
            {'user': user1, 'attraction': Attraction.objects.get(name='西湖')},
            {'user': user2, 'attraction': Attraction.objects.get(name='九寨沟')},
            {'user': user3, 'attraction': Attraction.objects.get(name='上海迪士尼乐园')},
            {'user': user1, 'attraction': Attraction.objects.get(name='兵马俑')},
        ]

        for data in favorite_data:
            if data['user'] and data['attraction']:
                favorite, created = Favorite.objects.get_or_create(
                    user=data['user'],
                    attraction=data['attraction'],
                )
                if created:
                    self.stdout.write(f'  - 创建收藏: {data["user"].username}@{data["attraction"].name}')

        # 6. 创建示例通知
        self.stdout.write('创建示例通知...')
        notification_data = [
            {'title': '系统公告', 'content': '欢迎使用旅游景点推荐系统，祝您旅途愉快！', 'type': 'SYSTEM', 'user': None},
            {'title': '景点更新', 'content': '九寨沟景区新增多处观景台，欢迎体验', 'type': 'ANNOUNCEMENT', 'user': None},
            {'title': '评论通知', 'content': '您的评论已通过审核', 'type': 'COMMENT', 'user': user1},
        ]

        for data in notification_data:
            notification, created = Notification.objects.get_or_create(
                title=data['title'],
                content=data['content'],
                type=data['type'],
                user=data['user'],
            )
            if created:
                user_info = data['user'].username if data['user'] else '全员'
                self.stdout.write(f'  - 创建通知: {data["title"]} -> {user_info}')

        # 输出统计
        self.stdout.write(self.style.SUCCESS('\n=== 数据统计 ==='))
        self.stdout.write(f'用户数量: {UserProfile.objects.filter(is_deleted=False).count()}')
        self.stdout.write(f'景点数量: {Attraction.objects.filter(is_deleted=False).count()}')
        self.stdout.write(f'评论数量: {Comment.objects.filter(is_deleted=False).count()}')
        self.stdout.write(f'收藏数量: {Favorite.objects.count()}')
        self.stdout.write(f'通知数量: {Notification.objects.filter(is_deleted=False).count()}')
        self.stdout.write(self.style.SUCCESS('\n初始化完成！'))
        self.stdout.write('\n测试账号:')
        self.stdout.write('  - 管理员: admin / admin123')
        self.stdout.write('  - 普通用户: user / user123')
