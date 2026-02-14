"""
景点评论批量导入命令

使用方法:
    python manage.py import_comments                    # 为所有景点生成评论(每个10条)
    python manage.py import_comments --count 15          # 每个景点15条
    python manage.py import_comments --attraction-id 1   # 为指定景点生成
    python manage.py import_comments --clear             # 先清空再生成
"""

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import UserProfile
from attractions.models import Attraction
from comments.models import Comment


# 评论模板 - 按景点类别
COMMENT_TEMPLATES = {
    "自然风光": [
        "风景太美了，空气清新怡人，值得一去！",
        "自然风光绝佳，拍照超级出片，推荐！",
        "环境非常好，就是周末人有点多，建议工作日去。",
        "值得推荐！风景如画，让人心旷神怡。",
        "山水相映，景色宜人，天然氧吧名不虚传。",
        "环境优美，空气清新，是放松身心的好地方。",
        "风景秀丽，拍照很出片，就是门票有点贵。",
        "自然景观保存得很好，强烈推荐！",
        "山清水秀，景色迷人，值得二刷！",
        "环境清幽，适合慢慢逛，放松心情。",
        "风景绝美，就是配套设施还需完善。",
        "大自然的鬼斧神工，太震撼了！",
        "空气清新，风景如画，遛娃好去处。",
        "景色很美，就是停车不太方便。",
        "天然氧吧名不虚传，身体和心灵都得到了放松。",
    ],
    "人文古迹": [
        "历史文化底蕴深厚，长知识了！",
        "建筑风格独特，非常震撼，感受到了历史的厚重。",
        "讲解很详细，让了解了很多历史故事。",
        "文化内涵丰富，不虚此行！",
        "古建筑保存完好，很值得参观。",
        "历史悠久，文化底蕴深厚，值得细细品味。",
        "建筑精美，细节之处见真章。",
        "很有历史年代感，仿佛穿越回古代。",
        "文化氛围浓厚，涨知识了！",
        "文物古迹保护得很好，点赞！",
        "历史价值很高，值得文化爱好者前来。",
        "建筑风格独特，拍照也很出片。",
        "讲解员专业，收获很多知识。",
        "很有教育意义，适合带孩子来学习。",
        "古色古香，非常有韵味的一个地方。",
    ],
    "主题乐园": [
        "游乐设施很丰富，玩得超级开心！",
        "适合亲子游，孩子特别喜欢！",
        "氛围感满满，体验超棒，推荐！",
        "项目刺激好玩，就是排队时间太长。",
        "环境整洁，服务态度好，体验不错。",
        "游玩的项目很多，一天根本玩不够！",
        "适合朋友聚会，玩的很开心！",
        "主题布置很用心，拍照很出片。",
        "设施维护得很好，安全措施到位。",
        "工作人员热情，互动活动很有趣。",
        "性价比高，值得二刷！",
        "孩子玩得不肯走，强烈推荐！",
        "氛围感十足，节日活动很有意思。",
        "刺激项目很多，胆大的朋友不要错过。",
        "整体体验很好，就是人太多了。",
    ],
    "其他": [
        "整体体验不错，值得推荐！",
        "环境优雅，服务周到。",
        "性价比还可以，会再来。",
        "地方很有特色，拍照很出片。",
        "环境不错，逛得很开心。",
        "设施齐全，体验感好。",
        "值得一去，氛围很好。",
        "服务态度好，很满意。",
        "环境整洁，舒适度高。",
        "很有特色，不虚此行。",
        "整体不错，推荐！",
        "休闲娱乐的好去处。",
        "环境好，玩的开心。",
        "值得推荐，体验很好。",
        "环境优雅，舒适宜人。",
    ],
}


class Command(BaseCommand):
    help = '批量生成景点评论数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='每个景点生成的评论数量(默认10)'
        )
        parser.add_argument(
            '--attraction-id',
            type=int,
            help='指定景点ID，为单个景点生成评论'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='生成前先清空现有评论'
        )

    def handle(self, *args, **options):
        count = options['count']
        attraction_id = options.get('attraction_id')
        clear = options.get('clear', False)

        # 清空评论
        if clear:
            Comment.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('已清空现有评论'))

        # 获取用户
        users = list(UserProfile.objects.filter(is_active=True, is_deleted=False))
        if not users:
            self.stdout.write(self.style.ERROR('没有找到活跃用户，请先创建用户'))
            return

        # 获取景点
        if attraction_id:
            attractions = Attraction.objects.filter(id=attraction_id, is_deleted=False)
        else:
            attractions = Attraction.objects.filter(is_deleted=False)

        attractions = list(attractions)
        if not attractions:
            self.stdout.write(self.style.ERROR('没有找到景点'))
            return

        self.stdout.write(f'开始为 {len(attractions)} 个景点生成评论...')

        total_comments = 0

        for attraction in attractions:
            # 获取景点类别
            category = attraction.category or "其他"
            templates = COMMENT_TEMPLATES.get(category, COMMENT_TEMPLATES["其他"])

            # 随机选择评论数量 (10-15 或指定数量)
            actual_count = count if count else random.randint(10, 15)

            # 如果模板不够，循环使用
            selected_templates = random.choices(templates, k=actual_count)

            comments_to_create = []
            base_time = timezone.now()

            for i, template in enumerate(selected_templates):
                # 随机选择用户
                user = random.choice(users)

                # 评分分布: 5分50%, 4分30%, 3分15%, 2分3%, 1分2%
                rating = random.choices(
                    [5, 4, 3, 2, 1],
                    weights=[50, 30, 15, 3, 2],
                    k=1
                )[0]

                # 状态分布: APPROVED 85%, PENDING 15%
                status = random.choices(
                    ['APPROVED', 'PENDING'],
                    weights=[85, 15],
                    k=1
                )[0]

                # 创建时间分散在最近30天内
                days_ago = random.randint(0, 30)
                created_at = base_time - timedelta(days=days_ago, hours=random.randint(0, 23))

                comments_to_create.append(
                    Comment(
                        user=user,
                        attraction=attraction,
                        content=template,
                        rating=rating,
                        status=status,
                        created_at=created_at,
                    )
                )

            # 批量创建
            Comment.objects.bulk_create(comments_to_create)
            total_comments += len(comments_to_create)

            self.stdout.write(
                f'  景点 "{attraction.name}" 生成了 {len(comments_to_create)} 条评论'
            )

        self.stdout.write(
            self.style.SUCCESS(f'完成！共生成 {total_comments} 条评论')
        )
