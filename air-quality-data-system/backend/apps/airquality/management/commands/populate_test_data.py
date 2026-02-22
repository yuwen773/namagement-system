import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.airquality.models import AirQualityData, City, MonitoringStation, Province
from apps.articles.models import Article, ArticleCategory
from apps.rules.models import ProtectionRule

User = get_user_model()


class Command(BaseCommand):
    help = "Populate the database with test data"

    def handle(self, *args, **options):
        self.stdout.write("Starting data population...")

        # 1. Create Users
        self.create_users()

        # 2. Create Location Data (Province, City, Station)
        self.create_locations()

        # 3. Create Air Quality Data
        self.create_air_quality_data()

        # 4. Create Articles
        self.create_articles()

        # 5. Create Protection Rules
        self.create_rules()

        self.stdout.write(self.style.SUCCESS("Data population completed successfully."))

    def create_users(self):
        self.stdout.write("Creating users...")
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            self.stdout.write(" - Created superuser: admin/admin123")

        if not User.objects.filter(username="testuser").exists():
            User.objects.create_user("testuser", "test@example.com", "test1234")
            self.stdout.write(" - Created normal user: testuser/test1234")

    def create_locations(self):
        self.stdout.write("Creating locations...")
        
        # Province
        province, created = Province.objects.get_or_create(
            code="110000",
            defaults={"name": "Beijing", "level": "Province"}
        )
        if created:
            self.stdout.write(f" - Created Province: {province.name}")

        # City
        city, created = City.objects.get_or_create(
            code="110100",
            defaults={
                "name": "Beijing City",
                "province": province,
                "longitude": 116.4074,
                "latitude": 39.9042
            }
        )
        if created:
            self.stdout.write(f" - Created City: {city.name}")

        # Stations
        stations_data = [
            {"code": "1001A", "name": "Wanliu", "address": "Haidian District", "type": "Urban"},
            {"code": "1002A", "name": "Dingling", "address": "Changping District", "type": "Suburban"},
            {"code": "1003A", "name": "Dongsi", "address": "Dongcheng District", "type": "Urban"},
        ]

        for s_data in stations_data:
            station, created = MonitoringStation.objects.get_or_create(
                code=s_data["code"],
                defaults={
                    "name": s_data["name"],
                    "city": city,
                    "address": s_data["address"],
                    "station_type": s_data["type"]
                }
            )
            if created:
                self.stdout.write(f" - Created Station: {station.name}")

    def create_air_quality_data(self):
        self.stdout.write("Creating air quality data...")
        stations = MonitoringStation.objects.all()
        end_time = timezone.now().replace(minute=0, second=0, microsecond=0)
        start_time = end_time - timedelta(days=7)

        # Generate data for the last 7 days, hourly
        current_time = start_time
        records_to_create = []
        
        while current_time <= end_time:
            for station in stations:
                if AirQualityData.objects.filter(station=station, monitor_time=current_time).exists():
                    continue

                # Simulate some realistic-ish data
                base_aqi = random.randint(30, 150)
                # Add some daily variation
                hour_factor = 1 + 0.5 * (12 - abs(current_time.hour - 12)) / 12
                aqi = int(base_aqi * hour_factor)
                aqi = max(0, min(500, aqi))

                pm25 = round(aqi * 0.6, 2)
                pm10 = round(aqi * 0.8, 2)
                
                records_to_create.append(AirQualityData(
                    station=station,
                    monitor_time=current_time,
                    aqi=aqi,
                    pm25=pm25,
                    pm10=pm10,
                    so2=random.uniform(5, 20),
                    no2=random.uniform(10, 40),
                    co=random.uniform(0.5, 2.0),
                    o3=random.uniform(20, 100),
                ))
            
            current_time += timedelta(hours=1)
            
            # Batch create every 24 hours to avoid memory issues if range is large
            if len(records_to_create) > 100:
                AirQualityData.objects.bulk_create(records_to_create)
                records_to_create = []

        if records_to_create:
            AirQualityData.objects.bulk_create(records_to_create)
            
        self.stdout.write(f" - Added air quality records for {stations.count()} stations.")

    def create_articles(self):
        self.stdout.write("Creating articles...")

        # Create categories
        categories = {
            "健康防护": 1,
            "科普知识": 2,
            "政策法规": 3,
        }

        for name, sort in categories.items():
            ArticleCategory.objects.get_or_create(
                name=name,
                defaults={"sort": sort}
            )

        # Articles data with announcements
        articles_data = [
            {
                "title": "系统维护通知",
                "content": "本系统将于每周日凌晨2:00-4:00进行例行维护，期间可能影响部分功能使用，敬请谅解。",
                "category": "健康防护",
                "is_announcement": True,
                "sort_order": 1,
                "status": Article.Status.PUBLISHED
            },
            {
                "title": "全国空气质量监测平台正式上线",
                "content": "全国空气质量数据监测与居民个人防护指南平台正式上线，为公众提供实时空气质量数据和健康防护建议。",
                "category": "健康防护",
                "is_announcement": True,
                "sort_order": 2,
                "status": Article.Status.PUBLISHED
            },
            {
                "title": "雾霾天气如何科学防护",
                "content": """
<h3>雾霾天气防护指南</h3>
<p>雾霾天气对健康影响较大，科学防护非常重要：</p>
<h4>1. 减少户外活动</h4>
<p>在雾霾天气时，应尽量减少户外活动时间，特别是儿童、老年人及患有心脑血管、呼吸系统疾病等易感人群。</p>
<h4>2. 佩戴防护口罩</h4>
<p>外出时应佩戴符合国家标准的防雾霾口罩（如KN95、N95等），并正确佩戴，确保口罩与面部贴合良好。</p>
<h4>3. 使用空气净化设备</h4>
<p>室内可使用空气净化器，选择具有HEPA滤网的产品，并定期更换滤芯。保持室内空气流通。</p>
<h4>4. 注意个人卫生</h4>
<p>外出归来后，应及时清洗面部、鼻腔和裸露皮肤，多喝水，多吃新鲜蔬菜水果，增强身体抵抗力。</p>
<h4>5. 及时就医</h4>
<p>如出现咳嗽、呼吸困难等症状加重时，应及时就医。</p>
                """,
                "category": "健康防护",
                "is_announcement": False,
                "sort_order": 0,
                "status": Article.Status.PUBLISHED
            },
            {
                "title": "AQI空气质量指数详解",
                "content": """
<h3>什么是AQI？</h3>
<p>AQI（Air Quality Index）是空气质量指数的缩写，是定量描述空气质量状况的无量纲指数。</p>
<h4>AQI分级标准</h4>
<ul>
<li><strong>0-50 优</strong>：空气质量令人满意，基本无空气污染</li>
<li><strong>51-100 良</strong>：空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响</li>
<li><strong>101-150 轻度污染</strong>：易感人群症状有轻度加剧，健康人群出现刺激症状</li>
<li><strong>151-200 中度污染</strong>：进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响</li>
<li><strong>201-300 重度污染</strong>：心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状</li>
<li><strong>301-500 严重污染</strong>：健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病</li>
</ul>
<h4>主要污染物</h4>
<p>参与AQI评价的主要污染物包括：细颗粒物（PM2.5）、可吸入颗粒物（PM10）、二氧化硫（SO2）、二氧化氮（NO2）、臭氧（O3）、一氧化碳（CO）。</p>
                """,
                "category": "科普知识",
                "is_announcement": False,
                "sort_order": 0,
                "status": Article.Status.PUBLISHED
            },
            {
                "title": "PM2.5的危害与防护",
                "content": """
<h3>PM2.5是什么？</h3>
<p>PM2.5是指环境空气中空气动力学当量直径小于等于2.5微米的颗粒物，也称细颗粒物。</p>
<h4>PM2.5的危害</h4>
<ul>
<li><strong>呼吸系统</strong>：可进入呼吸道深部，刺激和腐蚀肺泡壁，长期暴露可引发慢性支气管炎、肺气肿等疾病</li>
<li><strong>心血管系统</strong>：可进入血液循环，损伤血管内皮，增加心血管疾病风险</li>
<li><strong>致癌风险</strong>：PM2.5表面吸附的多环芳烃等有害物质具有致癌性</li>
<li><strong>免疫系统</strong>：降低人体免疫力，增加感染风险</li>
</ul>
<h4>防护措施</h4>
<ol>
<li>雾霾天气减少户外活动，特别是晨练</li>
<li>外出佩戴防霾口罩</li>
<li>室内使用空气净化器</li>
<li>多喝水，多吃润肺食物（如梨、银耳、百合等）</li>
<li>及时清理鼻腔和口腔</li>
</ol>
                """,
                "category": "科普知识",
                "is_announcement": False,
                "sort_order": 0,
                "status": Article.Status.PUBLISHED
            },
            {
                "title": "《环境空气质量标准》GB 3095-2012",
                "content": """
<h3>标准概述</h3>
<p>《环境空气质量标准》（GB 3095-2012）是我国现行环境空气质量标准，于2012年发布，2016年全面实施。</p>
<h4>主要变化</h4>
<ul>
<li>增加了PM2.5日均浓度限值和年均浓度限值</li>
<li>收紧了PM10、NO2等污染物的浓度限值</li>
<li>调整了数据有效性的相关规定</li>
<li>更新了空气质量指数（AQI）分级标准</li>
</ul>
<h4>标准意义</h4>
<p>该标准的实施标志着我国环境空气管理从总量控制向质量改善的转变，对推动大气污染防治工作具有重要意义。</p>
                """,
                "category": "政策法规",
                "is_announcement": False,
                "sort_order": 0,
                "status": Article.Status.PUBLISHED
            },
        ]

        articles_count = 0
        for a_data in articles_data:
            if not Article.objects.filter(title=a_data["title"]).exists():
                category = ArticleCategory.objects.get(name=a_data["category"])
                Article.objects.create(
                    category=category,
                    title=a_data["title"],
                    content=a_data["content"],
                    is_announcement=a_data["is_announcement"],
                    sort_order=a_data["sort_order"],
                    status=a_data["status"]
                )
                articles_count += 1

        self.stdout.write(f" - Created {articles_count} articles")

    def create_rules(self):
        self.stdout.write("Creating protection rules...")

        # AQI ranges based on HJ 633-2012 standard
        aqi_ranges = [
            (0, 50, "优"),
            (51, 100, "良"),
            (101, 150, "轻度污染"),
            (151, 200, "中度污染"),
            (201, 300, "重度污染"),
            (301, 500, "严重污染"),
        ]

        # Population types
        population_types = [
            (ProtectionRule.PopulationType.GENERAL, "一般人群"),
            (ProtectionRule.PopulationType.CHILDREN, "儿童"),
            (ProtectionRule.PopulationType.ELDERLY, "老年人"),
            (ProtectionRule.PopulationType.PATIENTS, "病患者"),
            (ProtectionRule.PopulationType.SENSITIVE, "敏感人群"),
        ]

        # Advice templates for each AQI range and population type
        advice_templates = {
            (0, 50, "GENERAL"): "空气质量优，可正常活动。多参加户外活动，呼吸新鲜空气。",
            (0, 50, "CHILDREN"): "空气质量优，适合户外活动。可正常进行户外游戏和运动。",
            (0, 50, "ELDERLY"): "空气质量优，适宜户外锻炼。建议进行适度的户外散步或运动。",
            (0, 50, "PATIENTS"): "空气质量优，适宜户外活动。可根据身体情况进行适度的户外活动。",
            (0, 50, "SENSITIVE"): "空气质量优，可正常户外活动。享受清新空气，进行有益的户外锻炼。",

            (51, 100, "GENERAL"): "空气质量良，可正常活动。极少数异常敏感人群应减少户外活动。",
            (51, 100, "CHILDREN"): "空气质量良好，可正常户外活动。极敏感儿童应减少长时间、高强度户外锻炼。",
            (51, 100, "ELDERLY"): "空气质量良好，适宜户外活动。极敏感老年人应减少长时间户外运动。",
            (51, 100, "PATIENTS"): "空气质量良好，可适度户外活动。极敏感患者应减少剧烈运动。",
            (51, 100, "SENSITIVE"): "空气质量良好，可正常活动。极敏感人群应减少长时间、高强度户外锻炼。",

            (101, 150, "GENERAL"): "轻度污染，敏感人群症状轻度加剧，健康人群出现刺激症状。建议儿童、老年人及心脏病、呼吸系统疾病患者减少长时间、高强度的户外锻炼。",
            (101, 150, "CHILDREN"): "轻度污染，建议减少户外活动。避免长时间户外运动，外出时建议佩戴防护口罩。",
            (101, 150, "ELDERLY"): "轻度污染，建议减少户外活动。有呼吸道疾病的老年人应避免户外锻炼，外出时做好防护。",
            (101, 150, "PATIENTS"): "轻度污染，建议减少户外活动。心脏病、呼吸系统疾病患者应避免户外运动，必要时外出需佩戴口罩。",
            (101, 150, "SENSITIVE"): "轻度污染，建议减少户外活动。敏感人群应避免户外运动，外出时做好防护措施。",

            (151, 200, "GENERAL"): "中度污染，进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响。建议儿童、老年人及心脏病、呼吸系统疾病患者避免长时间、高强度的户外锻炼，一般人群适量减少户外运动。",
            (151, 200, "CHILDREN"): "中度污染，避免户外活动。建议停止户外活动，尽量留在室内，关闭门窗。",
            (151, 200, "ELDERLY"): "中度污染，避免户外活动。老年人应避免户外锻炼，有基础疾病者应减少外出，注意休息。",
            (151, 200, "PATIENTS"): "中度污染，避免户外活动。心脏病、呼吸系统疾病患者应避免外出，注意监测健康状况，必要时就医。",
            (151, 200, "SENSITIVE"): "中度污染，避免户外活动。敏感人群应停止户外活动，留在室内并采取防护措施。",

            (201, 300, "GENERAL"): "重度污染，心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状。建议儿童、老年人和患有心脏病、肺病等易感人群停止户外活动，一般人群减少户外活动。",
            (201, 300, "CHILDREN"): "重度污染，停止所有户外活动。儿童应留在室内，避免体力消耗，保持室内空气流通。",
            (201, 300, "ELDERLY"): "重度污染，停止所有户外活动。老年人应留在室内休息，避免体力活动，注意健康监测。",
            (201, 300, "PATIENTS"): "重度污染，停止所有户外活动。心脏病、呼吸系统疾病患者应留在室内，避免体力活动，密切关注身体状况，必要时及时就医。",
            (201, 300, "SENSITIVE"): "重度污染，停止所有户外活动。敏感人群应留在室内，避免体力消耗，采取必要的防护措施。",

            (301, 500, "GENERAL"): "严重污染，健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病。建议儿童、老年人和患有心脏病、肺病等易感人群停止户外活动，一般人群停止户外活动。",
            (301, 500, "CHILDREN"): "严重污染，停止所有户外活动。儿童应留在室内，关闭门窗，使用空气净化器，避免任何户外接触。",
            (301, 500, "ELDERLY"): "严重污染，停止所有户外活动。老年人应留在室内，关闭门窗，使用空气净化设备，注意休息和健康监测。",
            (301, 500, "PATIENTS"): "严重污染，停止所有户外活动。心脏病、呼吸系统疾病患者应留在室内，关闭门窗，使用空气净化器，密切关注身体状况，随时准备就医。",
            (301, 500, "SENSITIVE"): "严重污染，停止所有户外活动。敏感人群应留在室内，关闭门窗，使用空气净化设备，避免任何户外接触。",
        }

        rules_count = 0
        for min_aqi, max_aqi, level_name in aqi_ranges:
            for pop_type, pop_name in population_types:
                advice = advice_templates.get((min_aqi, max_aqi, pop_type),
                    f"AQI {min_aqi}-{max_aqi}，{pop_name}请采取相应防护措施。")

                rule_name = f"{level_name}-{pop_name}"

                if not ProtectionRule.objects.filter(
                    population_type=pop_type,
                    min_aqi=min_aqi,
                    max_aqi=max_aqi
                ).exists():
                    ProtectionRule.objects.create(
                        rule_name=rule_name,
                        min_aqi=min_aqi,
                        max_aqi=max_aqi,
                        population_type=pop_type,
                        advice=advice,
                        is_enabled=True
                    )
                    rules_count += 1

        self.stdout.write(f" - Created {rules_count} protection rules (6 AQI ranges × 5 population types = 30 total)")
