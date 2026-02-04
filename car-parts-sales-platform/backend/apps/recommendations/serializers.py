"""
推荐管理序列化器
"""
from rest_framework import serializers
from .models import RecommendationRule, RecommendedProduct
from apps.products.serializers import ProductListSerializer


class RecommendationRuleSerializer(serializers.ModelSerializer):
    """推荐规则序列化器"""
    rule_type_display = serializers.CharField(source='get_rule_type_display', read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = RecommendationRule
        fields = [
            'id', 'name', 'rule_type', 'rule_type_display',
            'description', 'config', 'priority', 'limit',
            'is_active', 'product_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_product_count(self, obj):
        """获取关联的商品数量"""
        return obj.recommended_products.count()


class RecommendedProductSerializer(serializers.ModelSerializer):
    """推荐商品序列化器"""
    rule_name = serializers.CharField(source='rule.name', read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = RecommendedProduct
        fields = [
            'id', 'rule', 'rule_name', 'product',
            'sort_order', 'remark', 'created_at'
        ]
        read_only_fields = ['created_at']


class RecommendedProductCreateSerializer(serializers.ModelSerializer):
    """推荐商品创建序列化器（简化版）"""
    class Meta:
        model = RecommendedProduct
        fields = ['rule', 'product', 'sort_order', 'remark']


class RecommendationRuleDetailSerializer(serializers.ModelSerializer):
    """推荐规则详情序列化器（包含关联商品）"""
    rule_type_display = serializers.CharField(source='get_rule_type_display', read_only=True)
    recommended_products = serializers.SerializerMethodField()

    class Meta:
        model = RecommendationRule
        fields = [
            'id', 'name', 'rule_type', 'rule_type_display',
            'description', 'config', 'priority', 'limit',
            'is_active', 'recommended_products', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_recommended_products(self, obj):
        """获取关联的推荐商品列表"""
        products = obj.recommended_products.select_related('product').order_by('-sort_order')
        return RecommendedProductSerializer(products, many=True).data
