"""
商品模块的自定义过滤器
"""
from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    """
    商品过滤器
    支持按分类、价格区间、状态等筛选
    """
    # 支持逗号分隔的分类ID列表，如 category=1,2,3
    # 使用 CharFilter 接收字符串，然后自定义处理
    category = filters.CharFilter(method='filter_category')
    # 价格区间过滤
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['status', 'is_featured', 'is_new']

    def filter_category(self, queryset, name, value):
        """
        过滤分类，支持逗号分隔的多个分类ID
        如: category=1,2,3 会查询分类ID为1、2或3的商品
        """
        if value:
            # 将逗号分隔的字符串转换为整数列表
            category_ids = []
            for x in str(value).split(','):
                x = x.strip()
                if x.isdigit():
                    category_ids.append(int(x))

            if category_ids:
                # 使用 __in 查询多个分类
                return queryset.filter(category_id__in=category_ids)
        return queryset


class CategoryFilter(filters.FilterSet):
    """
    分类过滤器
    支持按父分类筛选、是否激活等
    """
    class Meta:
        model = Category
        fields = ['parent', 'is_active', 'sort_order']
