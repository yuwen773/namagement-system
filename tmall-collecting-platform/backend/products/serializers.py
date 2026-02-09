from rest_framework import serializers
from .models import Product, CrawlLog, PriceHistory


class ProductSerializer(serializers.ModelSerializer):
    """商品序列化器（完整版）"""
    price_display = serializers.SerializerMethodField()
    sales_display = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    region_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'product_id', 'title', 'price', 'price_unit', 'price_desc',
            'sales', 'shop', 'seller_nick', 'shop_tags', 'region',
            'tags', 'product_attributes', 'image_url', 'detail_url',
            'brand', 'category', 'batch_no', 'crawl_time',
            'created_at', 'updated_at',
            'price_display', 'sales_display', 'tags_list', 'region_display'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_price_display(self, obj):
        """格式化价格显示"""
        price_str = f"¥{obj.price}"
        if obj.price_unit:
            price_str += f"/{obj.price_unit}"
        if obj.price_desc:
            price_str += f" {obj.price_desc}"
        return price_str

    def get_sales_display(self, obj):
        """格式化销量显示"""
        if obj.sales >= 10000:
            return f"{obj.sales / 10000:.1f}万+"
        return f"{obj.sales}+"

    def get_tags_list(self, obj):
        """返回标签列表"""
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        return []

    def get_region_display(self, obj):
        """地区显示"""
        return obj.region or '未知'


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器（精简版）"""
    price_display = serializers.SerializerMethodField()
    sales_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'price_unit', 'sales', 'shop',
            'image_url', 'brand', 'category', 'region', 'tags',
            'crawl_time', 'price_display', 'sales_display'
        ]

    def get_price_display(self, obj):
        """格式化价格显示"""
        price_str = f"¥{obj.price}"
        if obj.price_unit:
            price_str += f"/{obj.price_unit}"
        return price_str

    def get_sales_display(self, obj):
        """格式化销量显示"""
        if obj.sales >= 10000:
            return f"{obj.sales / 10000:.1f}万+"
        return str(obj.sales)


class ProductCreateSerializer(serializers.ModelSerializer):
    """商品创建序列化器"""

    class Meta:
        model = Product
        fields = [
            'title', 'price', 'sales', 'shop',
            'image_url', 'detail_url', 'brand', 'category',
            'batch_no', 'crawl_time'
        ]

    def validate_price(self, value):
        """验证价格必须为正数"""
        if value <= 0:
            raise serializers.ValidationError("价格必须大于0")
        return value

    def validate_sales(self, value):
        """验证销量必须为非负整数"""
        if value < 0:
            raise serializers.ValidationError("销量不能为负数")
        return value


class CrawlLogSerializer(serializers.ModelSerializer):
    """采集日志序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)

    class Meta:
        model = CrawlLog
        fields = [
            'id', 'task_id', 'status', 'status_display',
            'mode', 'source_type', 'source_type_display',
            'start_time', 'end_time', 'items_collected',
            'items_success', 'items_failed', 'log_content',
            'error_message', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CrawlLogCreateSerializer(serializers.ModelSerializer):
    """采集日志创建序列化器"""

    class Meta:
        model = CrawlLog
        fields = ['task_id', 'status', 'mode', 'source_type']


class PriceHistorySerializer(serializers.ModelSerializer):
    """商品历史价格序列化器"""

    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'sales', 'record_date', 'created_at']
        read_only_fields = ['id', 'created_at']
