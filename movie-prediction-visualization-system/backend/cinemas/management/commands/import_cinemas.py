from django.core.management.base import BaseCommand
from cinemas.models import Region, Cinema
import random

class Command(BaseCommand):
    help = '导入地域和影院数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cinema-count',
            type=int,
            default=200,
            help='目标影院数量'
        )

    def handle(self, *args, **options):
        stats = {'regions': 0, 'cinemas': 0}

        self.stdout.write(self.style.HTTP_INFO("开始导入地域和影院数据..."))

        # 第一阶段：导入地域
        self.stdout.write(self.style.HTTP_INFO("\n=== 第一阶段：导入地域 ==="))
        self.import_regions(stats)

        # 第二阶段：生成影院
        self.stdout.write(self.style.HTTP_INFO("\n=== 第二阶段：生成影院 ==="))
        self.import_cinemas(options['cinema_count'], stats)

        self.stdout.write(self.style.SUCCESS(f"\n导入完成：地域 {stats['regions']} 个，影院 {stats['cinemas']} 家"))

    # ============= 地域数据 =============
    REGIONS_DATA = [
        # 直辖市
        {'name': '北京市', 'level': 'PROVINCE', 'children': ['东城区', '朝阳区', '海淀区', '丰台区']},
        {'name': '上海市', 'level': 'PROVINCE', 'children': ['黄浦区', '徐汇区', '浦东新区', '静安区']},
        {'name': '天津市', 'level': 'PROVINCE', 'children': ['和平区', '河西区', '南开区']},
        {'name': '重庆市', 'level': 'PROVINCE', 'children': ['渝中区', '江北区', '沙坪坝区']},
        # 华东
        {'name': '浙江省', 'level': 'PROVINCE', 'children': ['杭州市', '宁波市', '温州市']},
        {'name': '江苏省', 'level': 'PROVINCE', 'children': ['南京市', '苏州市', '无锡市']},
        {'name': '山东省', 'level': 'PROVINCE', 'children': ['济南市', '青岛市']},
        {'name': '福建省', 'level': 'PROVINCE', 'children': ['福州市', '厦门市', '泉州市']},
        {'name': '安徽省', 'level': 'PROVINCE', 'children': ['合肥市', '芜湖市']},
        # 华南
        {'name': '广东省', 'level': 'PROVINCE', 'children': ['广州市', '深圳市', '佛山市', '东莞市']},
        {'name': '广西壮族自治区', 'level': 'PROVINCE', 'children': ['南宁市', '桂林市', '柳州市']},
        {'name': '海南省', 'level': 'PROVINCE', 'children': ['海口市', '三亚市']},
        # 华中
        {'name': '湖北省', 'level': 'PROVINCE', 'children': ['武汉市', '宜昌市', '襄阳市']},
        {'name': '湖南省', 'level': 'PROVINCE', 'children': ['长沙市', '株洲市']},
        {'name': '河南省', 'level': 'PROVINCE', 'children': ['郑州市', '洛阳市', '开封市']},
        {'name': '江西省', 'level': 'PROVINCE', 'children': ['南昌市', '赣州市']},
        # 华北
        {'name': '河北省', 'level': 'PROVINCE', 'children': ['石家庄市', '唐山市', '秦皇岛市']},
        {'name': '山西省', 'level': 'PROVINCE', 'children': ['太原市', '大同市']},
        {'name': '内蒙古自治区', 'level': 'PROVINCE', 'children': ['呼和浩特市', '包头市']},
        # 西南
        {'name': '四川省', 'level': 'PROVINCE', 'children': ['成都市', '绵阳市', '德阳市']},
        {'name': '云南省', 'level': 'PROVINCE', 'children': ['昆明市', '大理市']},
        {'name': '贵州省', 'level': 'PROVINCE', 'children': ['贵阳市', '遵义市']},
        {'name': '西藏自治区', 'level': 'PROVINCE', 'children': ['拉萨市']},
        # 西北
        {'name': '陕西省', 'level': 'PROVINCE', 'children': ['西安市', '宝鸡市']},
        {'name': '甘肃省', 'level': 'PROVINCE', 'children': ['兰州市', '敦煌市']},
        {'name': '青海省', 'level': 'PROVINCE', 'children': ['西宁市']},
        {'name': '宁夏回族自治区', 'level': 'PROVINCE', 'children': ['银川市']},
        {'name': '新疆维吾尔自治区', 'level': 'PROVINCE', 'children': ['乌鲁木齐市']},
        # 东北
        {'name': '辽宁省', 'level': 'PROVINCE', 'children': ['沈阳市', '大连市', '鞍山市']},
        {'name': '吉林省', 'level': 'PROVINCE', 'children': ['长春市', '吉林市']},
        {'name': '黑龙江省', 'level': 'PROVINCE', 'children': ['哈尔滨市', '大庆市']},
    ]

    # ============= 影院品牌数据 =============
    CINEMA_CHAINS = {
        # 高端
        '万达影城': {'prefix': '万达影城', 'screen': (8, 15), 'seat': (1500, 3000), 'tier': 3},
        'CGV影城': {'prefix': 'CGV影城', 'screen': (7, 14), 'seat': (1300, 2800), 'tier': 3},
        '博纳国际影城': {'prefix': '博纳国际影城', 'screen': (7, 12), 'seat': (1200, 2500), 'tier': 3},
        'UME影城': {'prefix': 'UME影城', 'screen': (7, 13), 'seat': (1400, 2600), 'tier': 3},
        '中影国际影城': {'prefix': '中影国际影城', 'screen': (7, 14), 'seat': (1300, 2700), 'tier': 3},
        '耀莱成龙国际影城': {'prefix': '耀莱成龙国际影城', 'screen': (9, 16), 'seat': (1800, 3500), 'tier': 3},
        # 中端
        '大地影院': {'prefix': '大地影院', 'screen': (5, 10), 'seat': (800, 1800), 'tier': 2},
        '金逸影城': {'prefix': '金逸影城', 'screen': (6, 12), 'seat': (1000, 2200), 'tier': 2},
        '横店电影城': {'prefix': '横店电影城', 'screen': (6, 11), 'seat': (900, 2000), 'tier': 2},
        '上影影城': {'prefix': '上影影城', 'screen': (6, 12), 'seat': (1100, 2300), 'tier': 2},
        '星美国际影城': {'prefix': '星美国际影城', 'screen': (6, 10), 'seat': (1000, 1900), 'tier': 2},
        '保利万和电影院': {'prefix': '保利万和电影院', 'screen': (5, 9), 'seat': (800, 1600), 'tier': 2},
        '沃美影城': {'prefix': '沃美影城', 'screen': (6, 11), 'seat': (1000, 2000), 'tier': 2},
        '幸福蓝海国际影城': {'prefix': '幸福蓝海国际影城', 'screen': (6, 11), 'seat': (950, 2000), 'tier': 2},
        '苏宁影城': {'prefix': '苏宁影城', 'screen': (5, 10), 'seat': (900, 1800), 'tier': 2},
        '恒大嘉凯影城': {'prefix': '恒大嘉凯影城', 'screen': (7, 12), 'seat': (1200, 2400), 'tier': 2},
        '奥斯卡影城': {'prefix': '奥斯卡影城', 'screen': (5, 10), 'seat': (850, 1800), 'tier': 2},
        '长城国际影城': {'prefix': '长城国际影城', 'screen': (5, 9), 'seat': (850, 1700), 'tier': 2},
        '华人影城': {'prefix': '华人影城', 'screen': (5, 8), 'seat': (750, 1500), 'tier': 2},
        '金球影城': {'prefix': '金球影城', 'screen': (5, 8), 'seat': (800, 1500), 'tier': 2},
        '启航国际影城': {'prefix': '启航国际影城', 'screen': (5, 9), 'seat': (850, 1600), 'tier': 2},
        '博纳影业': {'prefix': '博纳影业', 'screen': (6, 11), 'seat': (1100, 2300), 'tier': 2},
        '传奇影城': {'prefix': '传奇影城', 'screen': (5, 9), 'seat': (850, 1700), 'tier': 2},
        # 艺术
        '百老汇电影中心': {'prefix': '百老汇电影中心', 'screen': (5, 9), 'seat': (600, 1300), 'tier': 2},
        '卢米埃影城': {'prefix': '卢米埃影城', 'screen': (4, 8), 'seat': (700, 1500), 'tier': 2},
        '美亚影城': {'prefix': '美亚影城', 'screen': (4, 7), 'seat': (600, 1200), 'tier': 2},
        '百老汇影院': {'prefix': '百老汇影院', 'screen': (4, 8), 'seat': (600, 1400), 'tier': 2},
        '新天地国际影城': {'prefix': '新天地国际影城', 'screen': (4, 8), 'seat': (650, 1400), 'tier': 2},
        '星光国际影城': {'prefix': '星光国际影城', 'screen': (4, 8), 'seat': (700, 1500), 'tier': 2},
        # 基础
        '今世界国际影城': {'prefix': '今世界国际影城', 'screen': (4, 7), 'seat': (600, 1100), 'tier': 1},
        '博悦影城': {'prefix': '博悦影城', 'screen': (4, 7), 'seat': (600, 1200), 'tier': 1},
        '银河电影院': {'prefix': '银河电影院', 'screen': (4, 7), 'seat': (650, 1300), 'tier': 1},
        '百花电影院': {'prefix': '百花电影院', 'screen': (3, 6), 'seat': (500, 1000), 'tier': 1},
        '大众影剧院': {'prefix': '大众影剧院', 'screen': (3, 6), 'seat': (500, 1000), 'tier': 1},
    }

    def import_regions(self, stats):
        """导入地域数据"""
        for province_data in self.REGIONS_DATA:
            # 创建省份
            province, created = Region.objects.get_or_create(
                name=province_data['name'],
                defaults={'level': 'PROVINCE', 'parent': None}
            )
            if created:
                stats['regions'] += 1

            # 创建城市
            for city_name in province_data['children']:
                city, created = Region.objects.get_or_create(
                    name=city_name,
                    defaults={'level': 'CITY', 'parent': province}
                )
                if created:
                    stats['regions'] += 1

        self.stdout.write(f"地域导入完成：{stats['regions']} 个")

    def import_cinemas(self, target_count, stats):
        """生成影院数据"""
        cities = list(Region.objects.filter(level='CITY'))

        if not cities:
            self.stdout.write(self.style.ERROR("请先导入地域数据！"))
            return

        # 城市等级分配权重
        city_weights = {}
        for city in cities:
            province_name = city.parent.name if city.parent else ''
            if province_name in ['北京市', '上海市']:  # 直辖市
                city_weights[city] = 5
            elif province_name in ['广东省', '浙江省', '江苏省', '四川省', '湖北省']:  # 省份
                if city.name in ['广州市', '深圳市']:  # 省内的重点城市
                    city_weights[city] = 5
                else:
                    city_weights[city] = 3
            elif province_name in ['山东省', '福建省', '河南省', '陕西省', '辽宁省']:
                city_weights[city] = 3
            else:
                city_weights[city] = 1

        # 初始化跳过计数器
        stats['skipped'] = 0

        for i in range(target_count):
            try:
                # 加权随机选择城市
                selected_city = random.choices(
                    cities,
                    weights=[city_weights.get(c, 1) for c in cities],
                    k=1
                )[0]

                # 随机选择品牌
                brand = random.choice(list(self.CINEMA_CHAINS.keys()))
                brand_info = self.CINEMA_CHAINS[brand]

                # 生成影院名称
                suffix = random.choice(['广场店', '购物中心店', '凯德店', '店', f'{selected_city.name}店'])
                cinema_name = f"{brand_info['prefix']}({selected_city.name}{suffix})"

                # 生成地址
                street = random.choice(['建设路', '人民路', '中山路', '解放路', '文化路', '商业街', '步行街', '广场路'])
                number = random.randint(1, 999)
                address = f"{selected_city.name}{street}{number}号"

                # 生成电话
                phone_prefix = random.choice(['010', '021', '020', '022', '023', '024', '025', '027', '028', '029', '0531', '0532', '0533', '0534', '0535', '0536', '0537', '0538', '0539', '0541', '0542', '0543', '0551', '0552', '0553', '0554', '0555', '0556', '0557', '0558', '0559', '0561', '0562', '0563', '0564', '0565', '0566', '0567', '0568', '0569', '0571', '0572', '0573', '0574', '0575', '0576', '0577', '0578', '0579', '0581', '0582', '0583', '0584', '0585', '0586', '0587', '0588', '0589', '0590', '0591', '0592', '0593', '0594', '0595', '0596', '0597', '0598'])
                phone = f"{phone_prefix}-{random.randint(10000000, 99999999)}"

                # 创建影院（使用 get_or_create 避免重复）
                cinema, created = Cinema.objects.get_or_create(
                    name=cinema_name,
                    defaults={
                        'address': address,
                        'phone': phone,
                        'region': selected_city,
                        'screen_count': random.randint(*brand_info['screen']),
                        'seats_count': random.randint(*brand_info['seat']),
                        'is_active': True
                    }
                )

                if created:
                    stats['cinemas'] += 1
                else:
                    stats['skipped'] += 1

                if stats['cinemas'] % 50 == 0:
                    self.stdout.write(f"已生成 {stats['cinemas']} 家影院...")

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"创建影院失败: {e}"))

        self.stdout.write(self.style.SUCCESS(f"影院生成完成：{stats['cinemas']} 家，跳过 {stats['skipped']} 家重复"))
