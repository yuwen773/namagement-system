"""
生成测试数据命令：告警、通知公告、节能知识
Usage: python manage.py generate_notices_and_alarms
"""
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.alarms.models import Alarm, AlarmRule, AlarmStatus, AlarmType, ConditionType
from apps.devices.models import Device, EnergyType
from apps.system.models import Notice, NoticePriority, NoticeTargetRole, NoticeType

User = get_user_model()


class Command(BaseCommand):
    help = "Generate test data: alarms, notices, and energy-saving knowledge"

    def handle(self, *args, **options):
        self.stdout.write("Starting data generation...")

        # 获取基础数据
        energy_types = {et.code: et for et in EnergyType.objects.all()}
        devices = list(Device.objects.all())
        users = list(User.objects.all())
        admin_user = users[0] if users else None

        # 确保有足够的设备
        if len(devices) < 10:
            self.stdout.write(self.style.ERROR("Not enough devices. Please import device data first."))
            return

        # 创建告警规则
        self.stdout.write("\n=== Creating Alarm Rules ===")
        rules = self.create_alarm_rules(energy_types)
        self.stdout.write(self.style.SUCCESS(f"Created {len(rules)} alarm rules"))

        # 生成告警数据
        self.stdout.write("\n=== Generating Alarms ===")
        alarms = self.generate_alarms(devices, rules, users)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(alarms)} alarm records"))

        # 生成通知公告
        self.stdout.write("\n=== Generating Notices ===")
        notices = self.generate_notices(admin_user)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(notices)} notices"))

        # 生成节能知识
        self.stdout.write("\n=== Generating Knowledge ===")
        knowledge = self.generate_knowledge(admin_user)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(knowledge)} energy-saving knowledge articles"))

        self.stdout.write(self.style.SUCCESS("\n=== Data generation completed! ==="))

    def create_alarm_rules(self, energy_types):
        """创建告警规则"""
        rules_data = [
            # 电能告警规则
            {"name": "电能用量过高告警", "energy_type": energy_types["ELECTRICITY"], "condition_type": ConditionType.THRESHOLD, "threshold_value": 1000},
            {"name": "电能用量突变告警", "energy_type": energy_types["ELECTRICITY"], "condition_type": ConditionType.MUTATION, "threshold_value": 50},
            {"name": "电能设备离线告警", "energy_type": energy_types["ELECTRICITY"], "condition_type": ConditionType.THRESHOLD, "threshold_value": 0},
            # 水能告警规则
            {"name": "水能用量过高告警", "energy_type": energy_types["WATER"], "condition_type": ConditionType.THRESHOLD, "threshold_value": 500},
            {"name": "水能用量突变告警", "energy_type": energy_types["WATER"], "condition_type": ConditionType.MUTATION, "threshold_value": 30},
            {"name": "水能设备离线告警", "energy_type": energy_types["WATER"], "condition_type": ConditionType.THRESHOLD, "threshold_value": 0},
            # 燃气告警规则
            {"name": "燃气用量过高告警", "energy_type": energy_types["GAS"], "condition_type": ConditionType.THRESHOLD, "threshold_value": 200},
            {"name": "燃气用量突变告警", "energy_type": energy_types["GAS"], "condition_type": ConditionType.MUTATION, "threshold_value": 20},
            {"name": "燃气设备离线告警", "energy_type": energy_types["GAS"], "condition_type": ConditionType.THRESHOLD, "threshold_value": 0},
        ]

        rules = []
        for data in rules_data:
            rule, created = AlarmRule.objects.get_or_create(
                name=data["name"],
                energy_type=data["energy_type"],
                condition_type=data["condition_type"],
                defaults={"threshold_value": data["threshold_value"], "is_active": True}
            )
            rules.append(rule)

        return rules

    def generate_alarms(self, devices, rules, users):
        """生成告警记录"""
        alarms = []
        now = timezone.now()

        # 告警类型分布
        alarm_types = [AlarmType.THRESHOLD, AlarmType.MUTATION, AlarmType.OFFLINE]
        statuses = [AlarmStatus.PENDING, AlarmStatus.PROCESSED, AlarmStatus.IGNORED]
        status_weights = [0.3, 0.5, 0.2]  # 待处理30%, 已处理50%, 已忽略20%

        # 告警描述模板
        alarm_descriptions = {
            AlarmType.THRESHOLD: [
                "用能超过阈值 {value}，请及时处理",
                "设备 {device} 能耗异常偏高",
                "当前用量 {value} 超过设定阈值",
                "检测到异常高能耗: {value}",
            ],
            AlarmType.MUTATION: [
                "用能突变 {value}%，请检查设备",
                "{device} 用能波动异常",
                "检测到用量突变: {value}%",
                "瞬时能耗变化超过阈值: {value}",
            ],
            AlarmType.OFFLINE: [
                "设备 {device} 已离线，请检查连接",
                "数据采集设备通讯中断",
                "设备 {device} 无法连接",
                "传感器离线，数据停止更新",
            ],
        }

        for i in range(40):
            device = random.choice(devices)
            rule = random.choice(rules)
            # 选择与设备能源类型匹配的规则
            matching_rules = [r for r in rules if r.energy_type == device.energy_type]
            if matching_rules:
                rule = random.choice(matching_rules)

            alarm_type = random.choice(alarm_types)
            status = random.choices(statuses, weights=status_weights)[0]

            # 生成告警时间（最近30天内）
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            alarm_time = now - timedelta(days=days_ago, hours=hours_ago)

            # 根据告警类型生成告警值
            if alarm_type == AlarmType.OFFLINE:
                alarm_value = None
            else:
                base_value = float(rule.threshold_value)
                alarm_value = round(base_value * random.uniform(1.1, 1.5), 2)

            # 生成描述
            description = random.choice(alarm_descriptions[alarm_type])
            description = description.format(device=device.name, value=alarm_value)

            # 创建告警
            alarm = Alarm.objects.create(
                device=device,
                rule=rule,
                alarm_type=alarm_type,
                alarm_value=alarm_value,
                alarm_time=alarm_time,
                status=status,
                handler=users[0] if status != AlarmStatus.PENDING and users else None,
                handle_time=alarm_time + timedelta(hours=random.randint(1, 48)) if status != AlarmStatus.PENDING else None,
                remark=description if status != AlarmStatus.PENDING else None,
            )
            alarms.append(alarm)

        return alarms

    def generate_notices(self, publisher):
        """生成通知公告"""
        notices = []

        notice_templates = [
            {
                "title": "关于开展2024年节能宣传周活动的通知",
                "content": """为深入贯彻落实国家节能降碳战略部署，提高全校师生节能意识，现定于5月13日至19日开展2024年节能宣传周活动。

活动主题："绿色校园，你我共建"

活动安排：
1. 节能知识讲座（周三下午3:00，行政楼报告厅）
2. 节能创意作品展（图书馆一楼展厅）
3. 校园节能自查行动（各院系自行组织）
4. 节能志愿者招募

请各部门高度重视，积极组织师生参与，共同为建设绿色校园贡献力量。

后勤管理处
2024年5月8日""",
                "priority": NoticePriority.HIGH
            },
            {
                "title": "夏季用电高峰安全提示",
                "content": """各位师生员工：

随着夏季高温天气到来，校园用电负荷持续攀升。为确保用电安全，现温馨提示如下：

1. 合理使用空调，室内温度设置不低于26℃，做到人走断电
2. 严禁使用大功率违禁电器
3. 定期检查办公区域用电设备，发现老化及时报修
4. 电动车充电请到指定区域，严禁室内充电
5. 遇到用电异常请及时联系后勤服务中心

如遇紧急停电，请保持冷静，听从现场工作人员指挥。

后勤管理处
2024年6月15日""",
                "priority": NoticePriority.URGENT
            },
            {
                "title": "能源计量系统升级维护通知",
                "content": """为提升能源管理效率，学校能源计量系统将于本周六进行升级维护。

维护时间：2024年3月16日（周六）22:00 - 次日6:00

影响范围：
- 线上能耗查询服务暂停
- 手机APP推送服务暂时中断
- 部分楼宇实时数据展示延迟

请各部门提前做好工作安排。系统升级完成后将恢复所有服务，对此给您带来的不便敬请谅解。

信息化管理中心
2024年3月14日""",
                "priority": NoticePriority.MEDIUM
            },
            {
                "title": "2024年第一季度能耗分析报告发布",
                "content": """各部门、各院系：

2024年第一季度校园能耗分析报告已编制完成，现予以发布。

主要数据：
- 第一季度总用电量：XX万kWh，同比下降3.2%
- 第一季度总用水量：XX万吨，同比下降5.1%
- 第一季度总用气量：XX万m³，同比下降2.8%

亮点工作：
1. 图书馆实施照明改造，节能效果显著
2. 宿舍区热水系统优化运行时间
3. 行政办公区试点智能空调节能系统

存在的问题：
1. 部分实验室能耗增长较快
2. 公共区域照明浪费现象仍有发生

请各部门对照分析报告，制定针对性节能措施。

节能工作领导小组办公室
2024年4月5日""",
                "priority": NoticePriority.MEDIUM
            },
            {
                "title": "关于开展用能情况自查的通知",
                "content": """各二级单位：

为全面掌握学校用能状况，推进节能降耗工作深入开展，现组织开展用能情况自查工作。

自查时间：2024年7月1日 - 7月15日

自查内容：
1. 本单位用能设备数量及运行情况
2. 2024年上半年能耗数据统计
3. 节能管理制度执行情况
4. 节能改造需求及建议

工作要求：
1. 高度重视，认真组织
2. 如实填报数据，确保准确性
3. 按时提交自查报告

请登录能源管理系统下载自查表格，填写完成后发送至节能办邮箱。

节能工作领导小组办公室
2024年6月25日""",
                "priority": NoticePriority.HIGH
            },
            {
                "title": "暑假期间用电安全注意事项",
                "content": """各位师生：

暑假将至，为确保假期校园用电安全，现将有关注意事项通知如下：

一、办公室区域
1. 离开前关闭所有用电设备电源
2. 拔掉长期不用的电器插头
3. 空调遥控器统一收缴保管

二、实验室区域
1. 24小时运行的设备需安排专人值守
2. 精密仪器做好防护措施
3. 危险化学品存储区域严禁使用非防爆电器

三、学生宿舍
1. 禁止使用热得快、电吹风等大功率电器
2. 离开宿舍前切断所有电源
3. 保管好个人贵重物品

四、报修服务
暑假期间后勤服务热线照常运行，报修电话：XXXX-XXXX。

祝大家度过一个安全、愉快的暑假！

保卫处 后勤管理处
2024年7月1日""",
                "priority": NoticePriority.HIGH
            },
            {
                "title": "校园路灯节能改造项目启动",
                "content": """各位师生：

为响应国家节能减排号召，推进绿色校园建设，学校将启动校园路灯节能改造项目。

项目概况：
- 改造范围：全校公共区域路灯
- 改造内容：将传统钠灯更换为LED节能灯具
- 预期效果：节能率可达60%以上

施工安排：
第一阶段：7月-8月（暑假期间），完成主干道改造
第二阶段：9月-10月，完成次干道及景观灯改造
第三阶段：11月-12月，完成宿舍区路灯改造

施工期间请注意安全，不要靠近施工区域。夜间照明将保持正常，不影响师生出行。

感谢您的理解与配合！

后勤管理处
2024年6月20日""",
                "priority": NoticePriority.MEDIUM
            },
            {
                "title": "能效管理平台培训通知",
                "content": """各院系、各部门：

为提高学校能源管理信息化水平，充分发挥能效管理平台功能，现组织平台操作培训。

培训时间：2024年4月18日（周四）下午2:30

培训地点：信息中心大楼302机房

培训内容：
1. 平台功能介绍及账号权限说明
2. 能耗数据查询与导出操作
3. 能耗报表制作与数据分析
4. 异常告警设置与处理

参加人员：各院系能源管理员、部门节能联络员

请各单位安排人员准时参加，确有特殊情况无法参加的，请提前向节能办请假。

联系人：张老师  电话：XXXX-XXXX

节能工作领导小组办公室
2024年4月10日""",
                "priority": NoticePriority.MEDIUM
            },
            {
                "title": "关于征集节能创意方案的通知",
                "content": """全体师生员工：

为调动广大师生参与节能降耗的积极性，推进节约型校园建设，现面向全校征集节能创意方案。

征集时间：2024年5月1日 - 5月31日

征集范围：
1. 建筑节能改造方案
2. 设备节能改进建议
3. 节能行为养成方案
4. 新能源利用设想
5. 其他节能创新思路

方案要求：
1. 符合学校实际，具有可操作性
2. 预期节能效果明显
3. 文字简洁，表述清晰
4. 可配示意图说明

奖项设置：
- 一等奖1名：奖金2000元
- 二等奖3名：奖金1000元
- 三等奖5名：奖金500元
- 优秀奖若干：纪念品一份

请将方案发送至节能办邮箱，邮件主题注明"节能创意方案"。

节能工作领导小组办公室
2024年4月25日""",
                "priority": NoticePriority.MEDIUM
            },
            {
                "title": "冬季供暖期间节能倡议书",
                "content": """老师们、同学们：

冬季供暖已经正式启动，为确保供暖效果的同时做好节能工作，我们向全校师生发出如下倡议：

一、合理调节室内温度
1. 办公区域温度控制在20℃左右
2. 宿舍区域温度控制在18℃-22℃
3. 无人时关闭暖气或调低温度

二、做好保温措施
1. 及时关闭门窗，防止热量流失
2. 不在暖气片上晾晒衣物
3. 不遮挡暖气片

三、养成节能习惯
1. 每天定时开窗通风，每次15-20分钟
2. 离开房间时关闭温控阀
3. 积极参加节能活动

四、及时报修
发现暖气不热、漏水等问题，请及时报修。

让我们共同努力，打造温暖、节能的校园环境！

后勤管理处
2024年11月15日""",
                "priority": NoticePriority.HIGH
            },
        ]

        notice_templates *= 4  # 复制4次以生成足够的数量

        now = timezone.now()
        for i, template in enumerate(notice_templates[:40]):
            days_ago = random.randint(0, 90)
            hours_ago = random.randint(0, 23)
            publish_time = now - timedelta(days=days_ago, hours=hours_ago)

            notice = Notice.objects.create(
                title=template["title"],
                content=template["content"],
                category="通知",
                notice_type=NoticeType.ANNOUNCEMENT,
                priority=template["priority"],
                publish_time=publish_time,
                is_published=True,
                publisher=publisher,
                target_role=NoticeTargetRole.ALL,
            )
            notices.append(notice)

        return notices

    def generate_knowledge(self, publisher):
        """生成节能知识文章"""
        knowledge_articles = [
            {
                "title": "空调使用十大节能技巧",
                "content": """炎炎夏日，空调成为耗电大户。以下是空调使用的十大节能技巧：

1. 合理设置温度
夏季制冷时，室内温度设置在26-28℃最为适宜，每升高1℃，可省电约10%。

2. 定期清洗过滤网
过滤网堵塞会增加能耗，建议每两周清洗一次。

3. 避免阳光直射
拉上窗帘或使用遮阳帘，可降低室内温度2-3℃。

4. 合理选择运行模式
制冷模式下，风速选择自动模式，制冷效果最佳且最省电。

5. 定时开关机
根据作息时间设置定时开关机，避免长时间空载运行。

6. 关闭门窗
确保房间密封性，减少冷气流失。

7. 利用睡眠模式
夜间使用睡眠模式，空调会自动调节温度，更省电。

8. 定期维护保养
请专业人员每年清洗空调内机，提高运行效率。

9. 选择合适匹数
根据房间面积选择合适匹数的空调，大马拉小车或小马拉大车都费电。

10. 出门提前关闭
出门前10分钟关闭空调，利用余冷保持室内温度。""",
                "category": "节能常识"
            },
            {
                "title": "办公室节能从细节做起",
                "content": """办公室是能耗大户，做好节能工作意义重大。以下是办公室节能的小贴士：

一、照明节能
1. 充分利用自然光，白天尽量不开灯
2. 随手关灯，离开办公室时检查是否关灯
3. 定期清洁灯具，提高照明效率
4. 办公区域分区控制，避免全开

二、设备节能
1. 电脑设置为节能模式，短暂离开时进入待机
2. 长时间不用时关闭电脑
3. 打印机集中打印，减少开关机次数
4. 饮水机随用随开，避免反复加热

三、空调节能
1. 空调温度设置合理，夏季不低于26℃
2. 开门开窗时关闭空调
3. 下班前20分钟关闭空调

四、其他节能
1. 减少一次性用品使用
2. 双面打印，节约用纸
3. 会议尽量采用线上方式
4. 养成节能意识，互相提醒监督

让我们共同努力，创建绿色办公环境！""",
                "category": "节能常识"
            },
            {
                "title": "学生宿舍节能指南",
                "content": """宿舍是我们日常生活的重要场所，养成良好的节能习惯受益终生。

一、用电安全
1. 禁止使用大功率违禁电器
2. 不私拉乱接电线
3. 电动车到指定区域充电
4. 离开宿舍切断电源

二、节约用电
1. 做到人走灯灭，随手关灯
2. 空调温度设置合理，不低于26℃
3. 电器不用时拔掉插头
4. 手机充电器不使用时拔下

三、节约用水
1. 洗衣服时集中洗涤
2. 洗手涂肥皂时关闭水龙头
3. 发现漏水及时报修
4. 养成节约用水的习惯

四、节能意识
1. 积极参加节能宣传活动
2. 互相提醒，养成节能习惯
3. 爱护宿舍公共设施
4. 共同营造节能宿舍氛围

节约资源是美德，更是责任。让我们从点滴做起！""",
                "category": "节能常识"
            },
            {
                "title": "照明节能改造全攻略",
                "content": """照明系统是建筑能耗的重要组成部分，照明节能改造可以带来显著的经济效益。

一、LED灯具优势
1. 节能效率高：相比白炽灯节能80%以上
2. 使用寿命长：可达5万小时
3. 光效高：光效可达100流明/瓦以上
4. 环保：无汞等有害物质

二、改造方案
1. 办公区域：采用LED面板灯
2. 教室：采用LED护眼教室灯
3. 走廊：采用LED吸顶灯或筒灯
4. 室外：采用LED路灯或庭院灯

三、智能控制
1. 安装红外感应开关，人来灯亮人走灯灭
2. 安装光照传感器，根据自然光调节灯光
3. 分区控制，按需开启
4. 时间控制，夜间定时开关

四、投资回报
以1000盏灯为例：
- 每年节约电费约15万元
- 投资回收期约2-3年
- 维护成本大幅降低

照明节能改造是一项一举多得的好事，值得推广！""",
                "category": "技术方案"
            },
            {
                "title": "智能水表应用与节水管理",
                "content": """水资源日益紧缺，智能水表的应用为节水管理提供了有力支撑。

一、智能水表功能
1. 实时监测用水量
2. 异常用水报警（漏水检测）
3. 数据远程传输
4. 用水数据分析

二、节水应用场景
1. 宿舍用水监测：发现异常用水及时提醒
2. 公共厕所：感应式冲水，避免浪费
3. 绿化灌溉：智能控制，按需浇水
4. 实验室用水：计量管理，责任到人

三、数据分析价值
1. 发现用水异常：及时发现跑冒滴漏
2. 用水规律分析：优化用水时间
3. 区域对比分析：找出用水大户
4. 考核依据：制定节水目标

四、实施建议
1. 分批次更换智能水表
2. 建立用水数据平台
3. 制定节水奖惩制度
4. 加强节水宣传教育

让每一滴水都发挥价值！""",
                "category": "技术方案"
            },
            {
                "title": "建筑保温与节能",
                "content": """建筑能耗占总能耗的比例越来越高，建筑保温是节能的重要环节。

一、建筑保温的重要性
1. 减少冬夏冷热损失
2. 提高空调供暖效率
3. 改善室内舒适度
4. 延长建筑使用寿命

二、主要保温措施
1. 外墙保温：采用保温砂浆或保温板
2. 屋面保温：使用挤塑聚苯板
3. 门窗保温：采用中空玻璃
4. 地板保温：特别是底层和架空层

三、既有建筑改造
1. 外墙外保温系统
2. 门窗更换为节能门窗
3. 屋面保温改造
4. 遮阳系统安装

四、节能效果
以100平方米住宅为例：
- 年可节约电费约500-800元
- 冬夏季室内温差可达3-5℃
- 空调运行时间减少约20%

建筑保温是一项长期投资，回报周期虽长但效益显著！""",
                "category": "技术方案"
            },
            {
                "title": "食堂节能管理要点",
                "content": """学校食堂是用能大户，做好节能工作意义重大。

一、燃气节能
1. 定期检查燃气管道，确保无泄漏
2. 合理安排烹饪时间，集中加工
3. 采用高效节能灶具
4. 余热回收利用

二、用电节能
1. 冷藏冷冻设备定期除霜
2. 展示柜夜间关闭
3. 照明分区分时控制
4. 电器设备定期维护

三、用水节能
1. 洗碗机集中清洗
2. 洗菜水回收利用
3. 龙头安装节水阀
4. 定期检查防止跑冒滴漏

四、管理措施
1. 建立节能管理制度
2. 加强员工节能培训
3. 设立节能目标考核
4. 推广节能新技术

五、典型案例
某高校食堂通过以下改造：
- 更换节能灶具，节气30%
- 安装智能控制，节电20%
- 优化加工流程，节水25%
- 年节约费用约15万元""",
                "category": "管理实践"
            },
            {
                "title": "实验室安全与节能",
                "content": """实验室是学校能耗较高的场所，安全与节能需要同时兼顾。

一、设备节能
1. 通风橱根据需要开启，不用时关闭
2. 超低温冰箱定期除霜，提高效率
3. 离心机满载运行，减少次数
4. 精密仪器按需预热

二、空调节能
1. 控制温湿度设定值
2. 夜间和节假日调高温度
3. 通风与空调协调运行
4. 定期维护保持效率

三、用电安全
1. 大功率设备专线供电
2. 不超负荷用电
3. 离开前检查断电
4. 定期检查电气线路

四、特种设备
1. 高压灭菌锅集中使用
2. 液氮罐定期检查补充
3. 气体钢瓶安全存放
4. 废气处理系统正常运行

五、管理建议
1. 建立实验室能耗档案
2. 制定节能操作规程
3. 加强人员培训
4. 开展节能评比""",
                "category": "管理实践"
            },
            {
                "title": "合同能源管理在校园的应用",
                "content": """合同能源管理（EMC）是一种新型的市场化节能机制，值得在校园推广。

一、什么是合同能源管理
1. 专业节能服务公司投资
2. 用能单位不出资
3. 节能效益分享
4. 合同期满设备移交

二、主要模式
1. 节能量保证型：达不到目标由公司赔偿
2. 节能效益分享型：按比例分享节能收益
3. 能源托管型：全面托管能源系统

三、适用项目
1. 照明系统改造
2. 空调系统改造
3. 供水系统改造
4. 监控系统升级

四、实施流程
1. 能源审计：评估节能潜力
2. 方案设计：制定改造方案
3. 合同签订：明确权责利
4. 项目实施：专业团队施工
5. 效果验收：监测节能效果

五、成功案例
某高校采用EMC模式：
- 照明改造投资300万元
- 年节电100万度
- 年节约电费80万元
- 5年回收投资

合同能源管理是实现校园节能的有效途径！""",
                "category": "技术方案"
            },
            {
                "title": "碳达峰碳中和知识问答",
                "content": """双碳目标是国家重大战略，让我们一起了解相关知识。

一、什么是碳达峰
碳达峰是指二氧化碳排放量达到历史最高值，之后逐步下降。

二、什么是碳中和
碳中和是指通过节能减排、植树造林等方式，抵消自身产生的二氧化碳排放。

三、为什么提出双碳目标
1. 应对气候变化挑战
2. 推动经济绿色转型
3. 保障能源安全
4. 实现可持续发展

四、节能与双碳的关系
1. 节能是最直接、最有效的减碳方式
2. 每节约1度电，减少约0.785kg碳排放
3. 每节约1吨标煤，减少约2.6吨碳排放
4. 节能就是减碳，节能就是环保

五、我们能做什么
1. 树立节能意识
2. 践行节能行动
3. 传播节能理念
4. 参与低碳活动

双碳目标人人有责，让我们共同行动！""",
                "category": "政策解读"
            },
            {
                "title": "节约用水知识手册",
                "content": """水是生命之源，节约用水是每个人的责任。

一、日常生活中怎么节水
1. 刷牙时关闭水龙头
2. 洗手涂肥皂时关闭水龙头
3. 洗菜水冲厕所
4. 洗衣机选择合适水位

二、卫生间节水
1. 安装节水马桶
2. 检查是否有漏水
3. 洗浴时间控制在10分钟内
4. 收集洗脸水冲厕所

三、厨房节水
1. 洗菜用盆接水
2. 洗碗时先擦后洗
3. 解冻食品提前取出
4. 煮面水涮碗

四、户外节水
1. 浇花时间安排在早晚
2. 洗车使用海绵和水桶
3. 雨水收集利用
4. 绿化采用滴灌

五、发现漏水怎么办
1. 及时报修
2. 记录水表读数
3. 跟踪维修进度
4. 确认修复效果

每一滴水都来之不易，让我们珍惜水资源！""",
                "category": "节能常识"
            },
            {
                "title": "智能建筑节能系统",
                "content": """智能建筑节能系统是现代建筑节能的重要手段。

一、系统组成
1. 能源监测平台
2. 智能照明系统
3. 楼宇自控系统
4. 环境监测系统

二、主要功能
1. 实时监测能耗数据
2. 自动调节设备运行
3. 异常报警提醒
4. 数据分析报表

三、应用场景
1. 照明控制：根据光照度和人员自动开关
2. 空调控制：根据室内外温度调节
3. 窗帘控制：根据光照度自动调节
4. 电梯控制：优化派梯减少空载

四、实施效益
以一栋5000平方米办公楼为例：
- 年节电约15-20%
- 年节约电费约10万元
- 设备寿命延长20%
- 维护成本降低30%

五、发展趋势
1. AI人工智能控制
2. 物联网技术应用
3. 大数据分析优化
4. 云平台远程管理

智能建筑让节能更简单！""",
                "category": "技术方案"
            },
        ]

        knowledge_articles *= 4  # 复制4次以生成足够的数量

        now = timezone.now()
        for i, article in enumerate(knowledge_articles[:40]):
            days_ago = random.randint(0, 180)
            hours_ago = random.randint(0, 23)
            publish_time = now - timedelta(days=days_ago, hours=hours_ago)

            notice = Notice.objects.create(
                title=article["title"],
                content=article["content"],
                category=article["category"],
                notice_type=NoticeType.KNOWLEDGE,
                priority=random.choice([NoticePriority.LOW, NoticePriority.MEDIUM]),
                publish_time=publish_time,
                is_published=True,
                publisher=publisher,
                target_role=NoticeTargetRole.ALL,
            )

        return []
