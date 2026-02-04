"""
数据填充脚本

为汽车改装件销售推荐平台生成模拟数据

生成数据包括：
- 20 个模拟用户（包含浏览记录、购物车、订单）
- 5 个管理员用户
- 3级商品分类
- 1000+ 商品数据
- 100+ 优惠券
- 50+ 改装案例
- 30+ FAQ

使用方法：
    cd backend
    python scripts/seed_data.py
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User, UserAddress
from apps.products.models import Category, Product, ProductImage, ProductAttribute, Review
from apps.orders.models import Order, OrderItem, Cart, CartItem
from apps.marketing.models import Coupon, UserCoupon
from apps.recommendations.models import RecommendationRule, RecommendedProduct
from apps.content.models import ModificationCase, FAQ
from apps.system.models import SystemConfig, Message, OperationLog


# ==================== 常量定义 ====================

# 模拟数据常量
NUM_USERS = 20
NUM_ADMINS = 5
NUM_PRODUCTS = 1000
NUM_COUPONS = 100
NUM_MODIFICATION_CASES = 50
NUM_FAQS = 30

# 中文数据源
LAST_NAMES = ['王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗']
FIRST_NAMES = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明', '超', '秀兰', '霞', '平', '刚', '桂英']

CITIES = [
    ('北京市', '北京市', ['朝阳区', '海淀区', '东城区', '西城区', '丰台区']),
    ('上海市', '上海市', ['浦东新区', '黄浦区', '徐汇区', '长宁区', '静安区']),
    ('广东省', '广州市', ['天河区', '越秀区', '海珠区', '荔湾区', '白云区']),
    ('广东省', '深圳市', ['福田区', '罗湖区', '南山区', '盐田区', '宝安区']),
    ('浙江省', '杭州市', ['西湖区', '上城区', '下城区', '江干区', '拱墅区']),
    ('江苏省', '南京市', ['玄武区', '秦淮区', '建邺区', '鼓楼区', '浦口区']),
    ('四川省', '成都市', ['锦江区', '青羊区', '金牛区', '武侯区', '成华区']),
]

# 商品分类名称（3级分类结构）
CATEGORY_DATA = {
    '发动机系统': {
        '进气系统': ['空气滤清器', '进气歧管', '节气门', '涡轮增压套件'],
        '排气系统': ['排气管', '消声器', '三元催化器', '尾喉'],
        '燃油系统': ['喷油嘴', '燃油泵', '燃油滤清器', '油箱'],
    },
    '底盘系统': {
        '悬挂系统': ['减震器', '弹簧', '控制臂', '稳定杆'],
        '制动系统': ['刹车片', '刹车盘', '刹车油', '刹车卡钳'],
        '转向系统': ['方向机', '转向拉杆', '转向助力泵'],
    },
    '车身外观': {
        '车身套件': ['前保险杠', '后保险杠', '侧裙', '尾翼', '引擎盖'],
        '灯光系统': ['LED大灯', '日间行车灯', '雾灯', '尾灯', '转向灯'],
        '车窗系统': ['车窗贴膜', '雨刮器', '后视镜'],
    },
    '内饰改装': {
        '座椅系统': ['赛车座椅', '座椅套', '座椅加热', '座椅通风'],
        '仪表系统': ['仪表盘', '仪表台', '换挡拨片', '踏板'],
        '音响系统': ['扬声器', '功放', '低音炮', '主机'],
    },
    '电子系统': {
        '行车电脑': ['ECU程序', '行车记录仪', 'OBD接口'],
        '导航系统': ['导航主机', 'GPS模块', '倒车雷达', '倒车影像'],
        '安防系统': ['防盗器', 'GPS定位器', '一键启动', '无钥匙进入'],
    },
    '轮胎轮毂': {
        '轮胎': ['夏季轮胎', '冬季轮胎', '全季轮胎', '性能轮胎'],
        '轮毂': ['铝合金轮毂', '钢制轮毂', '锻造轮毂', '旋压轮毂'],
        '配件': ['轮胎螺丝', '气门嘴', '轮毂装饰盖'],
    },
}

# 商品名称模板
PRODUCT_TEMPLATES = [
    "{brand} {category} 适用于{car_model}",
    "{brand} 高性能{category} {car_model}专用",
    "{brand} {category} 改装件 {car_model}",
    "原厂品质 {category} {brand} {car_model}",
    "{brand} 运动版{category} 适配{car_model}",
]

BRANDS = ['BOSCH', 'BREMBO', 'Eibach', 'KW', 'Bilstein', 'H&R', 'Akrapovic', 'Milltek', 'Remus', 'MagnaFlow',
          'K&N', 'BMC', 'AFE', 'Sprint Booster', 'RaceChip', 'JR', 'Forge', 'Dixon', 'Alcon', 'StopTech']

CAR_MODELS = [
    '宝马3系', '宝马5系', '奔驰C级', '奔驰E级', '奥迪A4', '奥迪A6', '大众高尔夫', '大众帕萨特',
    '本田思域', '本田雅阁', '丰田卡罗拉', '丰田凯美瑞', '福特福克斯', '马自达3', '马自达6',
    '斯巴鲁WRX', '三菱EVO', '日产GTR', '本田Type-R', '现代i30', '起亚福瑞迪'
]

# 商品描述模板
PRODUCT_DESCRIPTIONS = [
    "采用优质材料制造，经过严格质量检测，确保产品性能稳定可靠。",
    "专为高性能车辆设计，显著提升车辆动力性能和驾驶体验。",
    "原厂规格标准，直接替换安装，无需任何改装，方便快捷。",
    "采用先进工艺生产，表面处理精细，耐腐蚀，使用寿命长。",
    "经过赛道验证，性能卓越，是改装爱好者的理想选择。",
    "符合国际质量标准，通过多项认证，品质有保障。",
    "轻量化设计，减轻车身重量，提升车辆操控性能。",
    "优化空气动力学设计，提高车辆稳定性和燃油经济性。",
]

# 商品属性
PRODUCT_ATTRIBUTES = {
    '材质': ['铝合金', '不锈钢', '碳纤维', '钛合金', '铸铁', '橡胶', '塑料'],
    '颜色': ['黑色', '银色', '红色', '蓝色', '钛色', '原色', '红色+黑色'],
    '适用车型': CAR_MODELS,
    '品牌': BRANDS,
    '保修期': ['1年', '2年', '3年', '终身保修'],
    '产地': ['德国', '日本', '美国', '意大利', '中国', '英国'],
}

# 优惠券名称
COUPON_NAMES = [
    '新人专享券', '满减优惠', '折扣券', '免邮券', '限时特惠',
    '会员专享', '周年庆券', '回归礼包', '推荐有礼', '狂欢节券',
]

# 改装案例标题
CASE_TITLES = [
    '宝马M3性能升级方案', '奔驰C63 AMG改装案例', '奥迪S3动力提升',
    '高尔夫GTI Stage 2改装', '思域Type-R赛道化改装', '斯巴鲁WRX STI全方面升级',
    '福特福克斯ST改装', '马自达MX-5敞篷改装', '日产GTR宽体改装',
    '本田NSX超级跑车改装', '保时捷911 Turbo升级', '特斯拉Model 3性能改装',
]

# FAQ 问题
FAQ_QUESTIONS = {
    '订单问题': [
        ('如何取消订单？', '待付款和待发货状态的订单可以在订单详情页点击"取消订单"按钮进行取消。已发货的订单需要先申请退货。'),
        ('订单多久发货？', '一般情况下，订单付款后24-48小时内发货。定制商品可能需要3-5个工作日。'),
        ('如何查询订单物流？', '登录账户后，在"我的订单"中点击订单详情，可以看到物流信息和物流单号。'),
        ('订单可以修改收货地址吗？', '待付款状态可以修改收货地址，待发货及以上状态需要联系客服处理。'),
        ('部分发货怎么办？', '如果订单包含多个商品，可能会分开发货。您可以在订单详情中查看每个商品的发货状态。'),
    ],
    '支付问题': [
        ('支持哪些支付方式？', '我们支持支付宝、微信支付、银行卡等多种支付方式。'),
        ('支付失败了怎么办？', '请检查账户余额是否充足，或尝试更换支付方式。如仍有问题，请联系客服。'),
        ('可以开发票吗？', '可以，下单时请在备注中填写发票信息（抬头、税号）。'),
        ('货到付款吗？', '抱歉，目前暂不支持货到付款。'),
    ],
    '物流问题': [
        ('运费如何收取？', '单笔订单满199元免运费，不满199元收取10元运费（部分地区除外）。'),
        ('大概多久能收到货？', '一般情况下，发货后3-5天可收到货。偏远地区可能需要7-10天。'),
        ('可以指定快递吗？', '目前我们使用顺丰、中通、韵达等快递，暂不支持自选快递。'),
        ('发货地在哪里？', '我们的仓库位于上海、广州、北京等地，根据您的收货地址选择最近仓库发货。'),
    ],
    '商品问题': [
        ('商品是正品吗？', '所有商品均为正品，直接从品牌方或授权代理商采购，保证质量。'),
        ('商品有质保吗？', '所有商品提供质保服务，具体质保期请参考商品详情页。'),
        ('商品适用于我的车型吗？', '请在购买前确认商品适配车型，如有疑问可咨询客服。'),
        ('安装视频有吗？', '部分商品提供安装教程，请在商品详情页查看。'),
    ],
    '退换货问题': [
        ('支持7天无理由退货吗？', '未安装、未使用的商品支持7天无理由退货，已安装或定制商品不支持。'),
        ('如何申请退换货？', '在订单详情页点击"申请退换货"，填写原因并提交，客服会及时处理。'),
        ('退货运费谁承担？', '质量问题退换货由我们承担运费，其他原因退换货由买家承担。'),
        ('退款多久到账？', '退货确认后，1-3个工作日退款到原支付账户。'),
    ],
    '账户问题': [
        ('如何修改密码？', '在"个人中心-账户安全"中可以修改登录密码。'),
        ('忘记密码怎么办？', '点击登录页面的"忘记密码"，通过手机号验证码重置密码。'),
        ('如何修改收货地址？', '在"个人中心-收货地址管理"中可以新增、修改、删除地址。'),
        ('积分有什么用？', '积分可以在结算时抵扣现金，100积分=1元。'),
    ],
}


# ==================== 辅助函数 ====================

def random_phone():
    """生成随机手机号"""
    return f"1{random.choice([3,5,6,7,8,9])}{random.randint(100000000, 999999999)}"


def random_address():
    """生成随机地址"""
    province, city, districts = random.choice(CITIES)
    district = random.choice(districts)
    street = f"{random.choice(['建设路', '人民路', '解放路', '和平路', '文化路', '中山路', '南京路', '北京路'])}{random.randint(1, 999)}号"
    return province, city, district, street


def random_price(min_price=50, max_price=50000):
    """生成随机价格"""
    return Decimal(str(round(random.uniform(min_price, max_price), 2)))


def random_date(start_date, end_date):
    """生成随机日期"""
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )


def generate_product_name(category):
    """生成商品名称"""
    template = random.choice(PRODUCT_TEMPLATES)
    brand = random.choice(BRANDS)
    car_model = random.choice(CAR_MODELS)
    return template.format(brand=brand, category=category, car_model=car_model)


# ==================== 数据填充函数 ====================

def clear_existing_data():
    """清除现有数据"""
    print("正在清除现有数据...")
    Order.objects.all().delete()
    Cart.objects.all().delete()
    Review.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    User.objects.filter(is_superuser=True).delete()
    Coupon.objects.all().delete()
    ModificationCase.objects.all().delete()
    FAQ.objects.all().delete()
    RecommendationRule.objects.all().delete()
    SystemConfig.objects.all().delete()
    Message.objects.all().delete()
    OperationLog.objects.all().delete()
    print("现有数据清除完成！")


def create_admin_users():
    """创建管理员用户"""
    print(f"正在创建 {NUM_ADMINS} 个管理员用户...")

    admins = []
    for i in range(NUM_ADMINS):
        # 生成11位手机号: 188 + 8位数字
        phone = f"188{i:08d}"
        admin = User.objects.create(
            phone=phone,
            nickname=f"管理员{i+1}",
            password='admin123',  # 明文密码
            is_staff=True,
            is_superuser=True,
            is_active=True,
            points=random.randint(1000, 5000),
            status='active'
        )
        admins.append(admin)

    print(f"✓ 创建了 {len(admins)} 个管理员用户")
    return admins


def create_regular_users():
    """创建普通用户"""
    print(f"正在创建 {NUM_USERS} 个普通用户...")

    users = []
    for i in range(NUM_USERS):
        phone = random_phone()
        nickname = f"{random.choice(LAST_NAMES)}{random.choice(FIRST_NAMES)}"
        user = User.objects.create(
            phone=phone,
            nickname=nickname,
            password='123456',  # 明文密码
            is_staff=False,
            is_superuser=False,
            is_active=True,
            points=random.randint(0, 2000),
            status='active'
        )
        users.append(user)

    print(f"✓ 创建了 {len(users)} 个普通用户")
    return users


def create_user_addresses(users):
    """为用户创建收货地址"""
    print("正在为用户创建收货地址...")

    address_count = 0
    for user in users:
        # 每个用户1-3个地址
        num_addresses = random.randint(1, 3)
        for j in range(num_addresses):
            province, city, district, street = random_address()
            is_default = (j == 0)
            UserAddress.objects.create(
                user=user,
                recipient_name=user.nickname or f"收货人{random.randint(1, 999)}",
                phone=user.phone,
                province=province,
                city=city,
                district=district,
                address=f"{district}{street}",
                is_default=is_default
            )
            address_count += 1

    print(f"✓ 创建了 {address_count} 个收货地址")


def create_categories():
    """创建商品分类（3级结构）"""
    print("正在创建商品分类...")

    categories = {}  # 用于存储分类引用

    for level1_name, level2_data in CATEGORY_DATA.items():
        # 创建一级分类
        level1 = Category.objects.create(
            name=level1_name,
            parent=None,
            sort_order=random.randint(0, 100),
            is_active=True
        )
        categories[level1_name] = level1

        for level2_name, level3_items in level2_data.items():
            # 创建二级分类
            level2 = Category.objects.create(
                name=level2_name,
                parent=level1,
                sort_order=random.randint(0, 100),
                is_active=True
            )

            for level3_name in level3_items:
                # 创建三级分类
                Category.objects.create(
                    name=level3_name,
                    parent=level2,
                    sort_order=random.randint(0, 100),
                    is_active=True
                )

    category_count = Category.objects.count()
    print(f"✓ 创建了 {category_count} 个商品分类")
    return categories


def create_products():
    """创建商品数据"""
    print(f"正在创建 {NUM_PRODUCTS} 个商品数据...")

    # 获取所有三级分类
    leaf_categories = Category.objects.filter(children__isnull=True, is_active=True)

    if not leaf_categories.exists():
        print("⚠ 警告：没有找到叶子分类，跳过商品创建")
        return []

    products = []
    status_choices = ['draft', 'pending', 'published', 'archived']
    status_weights = [5, 10, 80, 5]  # 大部分商品为已上架状态

    for i in range(NUM_PRODUCTS):
        category = random.choice(leaf_categories)
        category_name = category.name

        # 生成商品名称
        product_name = generate_product_name(category_name)

        # 创建商品
        product = Product.objects.create(
            name=product_name,
            description=random.choice(PRODUCT_DESCRIPTIONS),
            price=random_price(50, 20000),
            original_price=random_price(100, 25000),
            category=category,
            stock_quantity=random.randint(0, 500),
            main_image=f"https://picsum.photos/seed/prod{i}/400/400.jpg",
            status=random.choices(status_choices, weights=status_weights)[0],
            sales_count=random.randint(0, 1000),
            view_count=random.randint(0, 5000),
            is_featured=random.random() < 0.2,  # 20%为推荐商品
            is_new=random.random() < 0.15,  # 15%为新品
        )
        products.append(product)

        # 创建商品图片（每个商品2-5张图片）
        num_images = random.randint(2, 5)
        for j in range(num_images):
            ProductImage.objects.create(
                product=product,
                image_url=f"https://picsum.photos/seed/prod{i}_{j}/400/400.jpg",
                sort_order=j
            )

        # 创建商品属性（每个商品3-6个属性）
        attributes = random.sample(list(PRODUCT_ATTRIBUTES.items()), k=random.randint(3, 6))
        for attr_name, attr_values in attributes:
            ProductAttribute.objects.create(
                product=product,
                attr_name=attr_name,
                attr_value=random.choice(attr_values),
                sort_order=random.randint(0, 50)
            )

    print(f"✓ 创建了 {len(products)} 个商品")
    print(f"  - 商品图片: {ProductImage.objects.count()} 张")
    print(f"  - 商品属性: {ProductAttribute.objects.count()} 个")
    return products


def create_coupons(users):
    """创建优惠券"""
    print(f"正在创建 {NUM_COUPONS} 个优惠券...")

    coupons = []
    now = timezone.now()

    for i in range(NUM_COUPONS):
        discount_type = random.choice(['full_reduction', 'discount'])
        is_active = random.random() < 0.8  # 80%的券可用

        coupon = Coupon.objects.create(
            name=f"{random.choice(COUPON_NAMES)}-{i+1:03d}",
            description=f"满{random.choice([100, 200, 300])}减{random.randint(10, 50)}优惠券",
            discount_type=discount_type,
            min_amount=Decimal(str(random.choice([0, 99, 199, 299, 499]))),
            discount_amount=Decimal(str(random.randint(5, 100))) if discount_type == 'full_reduction' else Decimal('0'),
            discount_rate=Decimal(str(round(random.uniform(0.7, 0.99), 2))) if discount_type == 'discount' else None,
            valid_from=now - timedelta(days=random.randint(0, 30)),
            valid_until=now + timedelta(days=random.randint(30, 180)),
            total_quantity=random.randint(100, 5000),
            per_user_limit=random.randint(1, 3),
            issued_quantity=random.randint(0, 500),
            is_active=is_active
        )
        coupons.append(coupon)

        # 为部分用户发放优惠券
        if is_active:
            num_users = random.randint(5, min(20, len(users)))
            selected_users = random.sample(users, num_users)
            for user in selected_users:
                UserCoupon.objects.get_or_create(
                    user=user,
                    coupon=coupon,
                    defaults={'status': 'unused'}
                )

    print(f"✓ 创建了 {len(coupons)} 个优惠券")
    print(f"  - 已发放用户优惠券: {UserCoupon.objects.count()} 张")


def create_carts_and_orders(users):
    """为用户创建购物车和订单"""
    print("正在为用户创建购物车和订单...")

    # 获取已上架的商品
    published_products = list(Product.objects.filter(status='published'))

    if not published_products:
        print("⚠ 警告：没有已上架的商品，跳过购物车和订单创建")
        return

    cart_count = 0
    order_count = 0
    review_count = 0

    for user in users:
        # 创建购物车
        cart, created = Cart.objects.get_or_create(user=user)
        if created:
            cart_count += 1

        # 添加商品到购物车（0-10个商品）
        num_cart_items = random.randint(0, 10)
        if num_cart_items > 0 and published_products:
            selected_products = random.sample(published_products, min(num_cart_items, len(published_products)))
            for product in selected_products:
                CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={
                        'product_name': product.name,
                        'product_image': product.main_image or '',
                        'price': product.price,
                        'quantity': random.randint(1, 3),
                    }
                )
            cart.update_totals()

        # 创建订单（0-5个订单）
        num_orders = random.randint(0, 5)
        user_addresses = list(user.addresses.all())

        for _ in range(num_orders):
            if not published_products or not user_addresses:
                break

            # 随机选择1-5个商品
            num_order_items = random.randint(1, 5)
            selected_products = random.sample(published_products, min(num_order_items, len(published_products)))
            address = random.choice(user_addresses)

            # 创建订单
            order = Order.objects.create(
                user=user,
                recipient_name=address.recipient_name,
                recipient_phone=address.phone,
                recipient_province=address.province,
                recipient_city=address.city,
                recipient_district=address.district,
                recipient_address=address.address,
                status=random.choice([
                    Order.Status.PENDING_PAYMENT,
                    Order.Status.PENDING_SHIPMENT,
                    Order.Status.SHIPPED,
                    Order.Status.COMPLETED,
                    Order.Status.CANCELLED,
                ]),
                # 状态权重分布
            )
            order_count += 1

            # 设置订单状态权重
            status_weights = [10, 20, 25, 40, 5]  # 更多已完成的订单
            order.status = random.choices(
                [Order.Status.PENDING_PAYMENT, Order.Status.PENDING_SHIPMENT,
                 Order.Status.SHIPPED, Order.Status.COMPLETED, Order.Status.CANCELLED],
                weights=status_weights
            )[0]

            # 如果是已发货或已完成，设置发货时间
            if order.status in [Order.Status.SHIPPED, Order.Status.COMPLETED]:
                order.shipped_at = random_date(order.created_at, timezone.now())
                order.express_company = random.choice(['顺丰速运', '中通快递', '韵达快递', '圆通速递'])
                order.tracking_number = f"{random.choice(['SF', 'ZT', 'YD', 'YT'])}{random.randint(1000000000, 9999999999)}"

            # 如果是已完成，设置完成时间
            if order.status == Order.Status.COMPLETED:
                order.paid_at = random_date(order.created_at, order.shipped_at or timezone.now())
                order.completed_at = random_date(order.shipped_at or order.paid_at, timezone.now())

            total_amount = Decimal('0')

            # 创建订单商品
            for product in selected_products:
                quantity = random.randint(1, 3)
                subtotal = product.price * quantity
                total_amount += subtotal

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_image=product.main_image or '',
                    product_price=product.price,
                    quantity=quantity,
                    subtotal=subtotal
                )

            order.total_amount = total_amount
            order.pay_amount = total_amount
            order.discount_amount = Decimal('0')
            order.shipping_fee = Decimal('0')
            order.save()

            # 为已完成的订单创建评价
            if order.status == Order.Status.COMPLETED:
                for item in order.items.all()[:random.randint(1, order.items.count())]:
                    if item.product and not Review.objects.filter(
                        product=item.product,
                        user_id=user.id,
                        order_item_id=item.id
                    ).exists():
                        Review.objects.create(
                            product=item.product,
                            user_id=user.id,
                            order_item_id=item.id,
                            rating=random.randint(3, 5),
                            comment=random.choice([
                                '质量很好，安装简单！',
                                '包装完好，发货迅速，商品给力！',
                                '性价比高，值得购买。',
                                '效果不错，推荐！',
                                '客服态度好，商品满意。',
                                '安装后效果明显，赞！',
                                '',  # 空评价
                            ]),
                            images=[f"https://picsum.photos/seed/review_{random.randint(1, 1000)}/200/200.jpg"]
                            if random.random() < 0.3 else [],
                            is_anonymous=random.random() < 0.5
                        )
                        review_count += 1

            # 增加商品销量和浏览量
            for item in order.items.all():
                if item.product:
                    item.product.sales_count += item.quantity
                    item.product.view_count += random.randint(1, 10)
                    item.product.save()

    print(f"✓ 创建了 {cart_count} 个购物车")
    print(f"✓ 创建了 {order_count} 个订单")
    print(f"✓ 创建了 {review_count} 个商品评价")


def create_recommendation_rules(products):
    """创建推荐规则"""
    print("正在创建推荐规则...")

    # 创建推荐规则
    rules = [
        {
            'name': '热门推荐',
            'rule_type': 'hot',
            'description': '根据销量和浏览量推荐热门商品',
            'config': {'min_sales': 50, 'min_views': 100},
            'priority': 100,
            'limit': 20,
        },
        {
            'name': '新品推荐',
            'rule_type': 'new',
            'description': '推荐最新上架的商品',
            'config': {'days': 30},
            'priority': 90,
            'limit': 15,
        },
        {
            'name': '精选推荐',
            'rule_type': 'personalized',
            'description': '编辑精选的高品质改装件',
            'config': {'featured_only': True},
            'priority': 80,
            'limit': 10,
        },
    ]

    created_rules = []
    for rule_data in rules:
        rule = RecommendationRule.objects.create(**rule_data)
        created_rules.append(rule)

        # 为规则添加推荐商品
        if products:
            num_products = min(rule_data['limit'], len(products))
            selected_products = random.sample(products, num_products)
            for i, product in enumerate(selected_products):
                RecommendedProduct.objects.create(
                    rule=rule,
                    product=product,
                    sort_order=num_products - i,
                    remark=f'自动推荐商品-{i+1}'
                )

    print(f"✓ 创建了 {len(created_rules)} 个推荐规则")
    print(f"✓ 添加了 {RecommendedProduct.objects.count()} 个推荐商品")


def create_modification_cases():
    """创建改装案例"""
    print(f"正在创建 {NUM_MODIFICATION_CASES} 个改装案例...")

    case_contents = [
        "本次改装项目包括进气系统升级、排气系统优化以及ECU程序调校。经过专业技师调试，车辆动力提升了约15%，扭矩输出更加线性。全套改装采用原厂位安装，不影响车辆质保。",
        "外观方面安装了前唇、侧裙和后扰流板，配合悬挂系统的降低，整体姿态更加运动。轮毂升级为19寸锻造轮毂，搭配高性能轮胎，提升了操控性能。",
        "内饰升级了赛车座椅、方向盘和仪表盘。音响系统更换了高端品牌扬声器，配合功放和低音炮，音质有了显著提升。",
        "刹车系统升级为大四活塞卡钳和高性能刹车片，配合高性能轮胎，制动距离明显缩短，提升了行车安全性。",
        "全套LED灯光系统升级，包括大灯、日间行车灯、转向灯和尾灯。亮度提升，能耗降低，夜间行车更加安全。",
        "涡轮增压套件安装，配合中冷器和进气管路升级。经过专业调校，马力提升了50匹，百公里加速缩短了0.8秒。",
        "悬挂系统更换为绞牙避震，可调节高度和阻尼。降低了车身高度，提升了过弯稳定性，日常驾驶舒适性也保持良好。",
        "排气系统采用全段不锈钢排气管，声浪低沉有力，不扰民。配合高流量三元催化，排气更加顺畅。",
    ]

    cases = []
    for i in range(NUM_MODIFICATION_CASES):
        is_published = random.random() < 0.8
        published_date = random_date(timezone.now() - timedelta(days=365), timezone.now()) if is_published else None

        case = ModificationCase.objects.create(
            title=f"{random.choice(CASE_TITLES)} - {i+1:03d}",
            summary=f"这是一份关于{random.choice(['宝马', '奔驰', '奥迪', '大众', '本田'])}的改装案例，展示了专业的改装工艺和显著的性能提升。",
            content=random.choice(case_contents),
            cover_image=f"https://picsum.photos/seed/case{i}/800/600.jpg",
            author=random.choice(['张技师', '李工', '王师傅', '赵工程师', '刘技师']),
            status='published' if is_published else 'draft',
            view_count=random.randint(0, 5000) if is_published else 0,
            sort_order=random.randint(0, 100),
            published_at=published_date
        )
        cases.append(case)

    print(f"✓ 创建了 {len(cases)} 个改装案例")


def create_faqs():
    """创建常见问题"""
    print(f"正在创建 {NUM_FAQS} 个常见问题...")

    faqs = []
    faq_index = 0

    for category, questions in FAQ_QUESTIONS.items():
        for question, answer in questions:
            if faq_index >= NUM_FAQS:
                break

            FAQ.objects.create(
                question=question,
                answer=answer,
                category=category,
                sort_order=random.randint(0, 100),
                is_active=True
            )
            faq_index += 1
            faqs.append((question, category))

    # 如果FAQ数量不够，添加一些额外的FAQ
    extra_questions = [
        ('其他', '如何联系客服？', '您可以通过在线客服、客服电话400-123-4567或微信公众号联系我们。'),
        ('其他', '营业时间是什么时候？', '客服工作时间：周一至周五 9:00-18:00，节假日正常休息。'),
        ('其他', '有实体店吗？', '我们在北京、上海、广州、深圳均有实体店，欢迎到店体验。'),
        ('其他', '可以上门安装吗？', '部分地区提供上门安装服务，下单前请咨询客服确认。'),
        ('其他', '产品质量有保证吗？', '所有商品均为正品，提供质保服务，质量问题支持退换货。'),
    ]

    for category, question, answer in extra_questions:
        if faq_index >= NUM_FAQS:
            break
        FAQ.objects.create(
            question=question,
            answer=answer,
            category=category,
            sort_order=random.randint(0, 100),
            is_active=True
        )
        faq_index += 1

    print(f"✓ 创建了 {FAQ.objects.count()} 个常见问题")


def create_system_configs():
    """创建系统配置"""
    print("正在创建系统配置...")

    configs = [
        # 基础配置
        ('site_name', '汽车改装件销售平台', 'basic', True),
        ('site_title', '专业汽车改装件电商平台 - 改装件商城', 'basic', True),
        ('site_keywords', '汽车改装,改装件,汽车配件,性能改装,外观改装', 'basic', True),
        ('site_description', '专业的汽车改装件电商平台，提供发动机系统、底盘系统、车身外观、内饰改装等各类汽车改装配件。', 'basic', True),
        ('contact_phone', '400-123-4567', 'basic', True),
        ('contact_email', 'service@autoparts.com', 'basic', True),
        ('company_address', '北京市朝阳区改装产业园123号', 'basic', True),

        # 交易配置
        ('min_order_amount', '99', 'trade', True),
        ('free_shipping_amount', '199', 'trade', True),
        ('shipping_fee', '10', 'trade', True),
        ('order_auto_cancel_hours', '24', 'trade', True),
        ('order_auto_complete_days', '7', 'trade', True),

        # 其他配置
        ('copyright', '© 2024 汽车改装件销售平台 版权所有', 'other', True),
        ('icp_license', '京ICP备12345678号', 'other', True),
        ('version', '1.0.0', 'other', False),
    ]

    for key, value, category, is_editable in configs:
        SystemConfig.objects.get_or_create(
            key=key,
            defaults={
                'value': value,
                'category': category,
                'is_editable': is_editable,
            }
        )

    print(f"✓ 创建了 {len(configs)} 个系统配置")


def create_system_messages(users):
    """创建系统消息"""
    print("正在创建系统消息...")

    messages = [
        ('系统公告', '欢迎使用汽车改装件销售平台！新用户注册即送100积分优惠券。', 'announcement'),
        ('促销通知', '限时特惠活动开启！全场满500减50，满1000减120。快来选购吧！', 'promotion'),
        ('系统通知', '平台将于2024年2月1日00:00-02:00进行系统维护，期间可能影响部分功能使用。', 'system'),
    ]

    for title, content, msg_type in messages:
        # 创建全员消息
        Message.objects.create(
            recipient=None,  # None表示全员消息
            title=title,
            content=content,
            message_type=msg_type,
            status='sent',
            sent_at=timezone.now()
        )

    # 为部分用户创建个性化消息
    if users:
        num_users = min(5, len(users))
        selected_users = random.sample(users, num_users)
        for user in selected_users:
            Message.objects.create(
                recipient=user,
                title='订单通知',
                content=f'尊敬的{user.nickname}，您有一个订单已发货。',
                message_type='notification',
                status='sent',
                sent_at=timezone.now()
            )

    print(f"✓ 创建了 {Message.objects.count()} 个系统消息")


def create_operation_logs(admins):
    """创建操作日志"""
    print("正在创建操作日志...")

    actions = [
        ('create', 'Product', '创建商品'),
        ('update', 'Product', '更新商品'),
        ('delete', 'Product', '删除商品'),
        ('create', 'Category', '创建分类'),
        ('update', 'Order', '处理订单'),
        ('login', 'User', '管理员登录'),
        ('update', 'Coupon', '更新优惠券'),
    ]

    for admin in admins:
        # 每个管理员生成10-30条操作日志
        num_logs = random.randint(10, 30)
        for _ in range(num_logs):
            action_type, object_type, detail = random.choice(actions)
            log_date = random_date(timezone.now() - timedelta(days=30), timezone.now())

            OperationLog.objects.create(
                operator=admin,
                action_type=action_type,
                object_type=object_type,
                object_id=str(random.randint(1, 1000)),
                detail=detail,
                ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                status='success',
                created_at=log_date
            )

    print(f"✓ 创建了 {OperationLog.objects.count()} 个操作日志")


# ==================== 主函数 ====================

def print_summary():
    """打印数据统计摘要"""
    print("\n" + "="*60)
    print("数据填充完成！统计摘要：")
    print("="*60)

    print(f"\n【用户数据】")
    print(f"  - 管理员用户: {User.objects.filter(is_staff=True, is_superuser=True).count()} 个")
    print(f"  - 普通用户: {User.objects.filter(is_staff=False).count()} 个")
    print(f"  - 收货地址: {UserAddress.objects.count()} 个")

    print(f"\n【商品数据】")
    print(f"  - 商品分类: {Category.objects.count()} 个")
    print(f"  - 商品: {Product.objects.count()} 个")
    print(f"  - 商品图片: {ProductImage.objects.count()} 张")
    print(f"  - 商品属性: {ProductAttribute.objects.count()} 个")

    print(f"\n【订单数据】")
    print(f"  - 购物车: {Cart.objects.count()} 个")
    print(f"  - 购物车商品: {CartItem.objects.count()} 个")
    print(f"  - 订单: {Order.objects.count()} 个")
    print(f"  - 订单商品: {OrderItem.objects.count()} 个")
    print(f"  - 商品评价: {Review.objects.count()} 个")

    print(f"\n【营销数据】")
    print(f"  - 优惠券: {Coupon.objects.count()} 个")
    print(f"  - 用户优惠券: {UserCoupon.objects.count()} 张")

    print(f"\n【推荐数据】")
    print(f"  - 推荐规则: {RecommendationRule.objects.count()} 个")
    print(f"  - 推荐商品: {RecommendedProduct.objects.count()} 个")

    print(f"\n【内容数据】")
    print(f"  - 改装案例: {ModificationCase.objects.count()} 个")
    print(f"  - 常见问题: {FAQ.objects.count()} 个")

    print(f"\n【系统数据】")
    print(f"  - 系统配置: {SystemConfig.objects.count()} 个")
    print(f"  - 系统消息: {Message.objects.count()} 个")
    print(f"  - 操作日志: {OperationLog.objects.count()} 条")

    print("\n" + "="*60)
    print("测试账号信息：")
    print("="*60)

    admins = User.objects.filter(is_staff=True, is_superuser=True)
    if admins.exists():
        print("\n管理员账号（任选其一）：")
        for admin in admins[:3]:
            print(f"  手机号: {admin.phone}")
            print(f"  密码: admin123")

    users = User.objects.filter(is_staff=False)
    if users.exists():
        print("\n普通用户账号（任选其一）：")
        for user in users[:3]:
            print(f"  手机号: {user.phone}")
            print(f"  密码: 123456")

    print("\n" + "="*60)


def main():
    """主函数"""
    print("\n" + "="*60)
    print("汽车改装件销售平台 - 数据填充脚本")
    print("="*60 + "\n")

    # 询问是否清除现有数据
    response = input("是否清除现有数据？这将删除所有现有数据！(yes/no): ").strip().lower()
    if response == 'yes':
        clear_existing_data()
    else:
        print("保留现有数据，继续填充...\n")

    try:
        print("开始填充数据...\n")

        # 1. 创建用户
        admins = create_admin_users()
        users = create_regular_users()

        # 2. 创建用户地址
        create_user_addresses(users)

        # 3. 创建商品分类
        categories = create_categories()

        # 4. 创建商品
        products = create_products()

        # 5. 创建优惠券
        create_coupons(users)

        # 6. 创建购物车和订单
        create_carts_and_orders(users)

        # 7. 创建推荐规则
        create_recommendation_rules(products)

        # 8. 创建改装案例
        create_modification_cases()

        # 9. 创建常见问题
        create_faqs()

        # 10. 创建系统配置
        create_system_configs()

        # 11. 创建系统消息
        create_system_messages(users)

        # 12. 创建操作日志
        create_operation_logs(admins)

        # 打印统计摘要
        print_summary()

        print("\n✅ 数据填充完成！\n")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
