"""
数据统计API视图 - 优化版
提供丰富的数据分析接口
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q

from .models import Product
from .analytics import ProductAnalytics
from users.permissions import IsAdminUser


class APIResponseMixin:
    """统一API响应格式"""

    def success_response(self, data=None, message="操作成功", total=None):
        response_data = {"code": 0, "message": message}
        if data is not None:
            response_data["data"] = data
        if total is not None:
            response_data["total"] = total
        return Response(response_data)

    def error_response(self, message="操作失败", code=-1):
        return Response({"code": code, "message": message}, status=status.HTTP_400_BAD_REQUEST)


class StatisticsOverviewView(APIResponseMixin, APIView):
    """数据统计概览（增强版）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取增强的统计概览数据"""
        # 获取查询参数
        search = request.query_params.get('search', '')
        brand = request.query_params.get('brand')
        region = request.query_params.get('region')

        # 构建查询集
        queryset = Product.objects.all()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(shop__icontains=search)
            )

        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        if region:
            queryset = queryset.filter(region__icontains=region)

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_overview()

        return self.success_response(data)


class StatisticsPriceDistributionView(APIResponseMixin, APIView):
    """价格区间分布统计（智能区间）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取智能价格区间分布"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        brand = request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_price_distribution()

        return self.success_response(data)


class StatisticsSalesDistributionView(APIResponseMixin, APIView):
    """销量区间分布统计（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取销量区间分布"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_sales_distribution()

        return self.success_response(data)


class StatisticsBrandAnalysisView(APIResponseMixin, APIView):
    """品牌分析（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取品牌详细分析"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 获取Top N
        top_n = int(request.query_params.get('top_n', 15))

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_brand_analysis(top_n=top_n)

        return self.success_response(data, total=len(data))


class StatisticsRegionAnalysisView(APIResponseMixin, APIView):
    """地区分析（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取地区详细分析"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 获取Top N
        top_n = int(request.query_params.get('top_n', 15))

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_region_analysis(top_n=top_n)

        return self.success_response(data, total=len(data))


class StatisticsShopAnalysisView(APIResponseMixin, APIView):
    """店铺分析（增强版）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取店铺详细分析"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(shop__icontains=search)
            )

        # 获取Top N
        top_n = int(request.query_params.get('top_n', 20))

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_shop_analysis(top_n=top_n)

        return self.success_response(data, total=len(data))


class StatisticsTopProductsView(APIResponseMixin, APIView):
    """Top商品（增强版 - 支持多维度排序）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取Top商品"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 排序方式
        sort_by = request.query_params.get('sort_by', 'sales')
        top_n = int(request.query_params.get('top_n', 20))

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_top_products(top_n=top_n, sort_by=sort_by)

        return self.success_response(data, total=len(data))


class StatisticsPriceSalesCorrelationView(APIResponseMixin, APIView):
    """价格-销量关联分析（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取价格与销量的关联分析"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_price_sales_correlation()

        return self.success_response(data)


class StatisticsAttributeAnalysisView(APIResponseMixin, APIView):
    """商品属性分析（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取商品属性统计分析"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_attribute_analysis()

        return self.success_response(data)


class StatisticsBatchAnalysisView(APIResponseMixin, APIView):
    """批次分析（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取批次分析数据"""
        queryset = Product.objects.all()

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_batch_analysis()

        return self.success_response(data, total=len(data))


class StatisticsKeywordAnalysisView(APIResponseMixin, APIView):
    """关键词分析（新增）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取标题关键词分析"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)

        # 获取Top N
        top_n = int(request.query_params.get('top_n', 30))
        sample_size = int(request.query_params.get('sample_size', 200))

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_keyword_analysis(top_n=top_n, sample_size=sample_size)

        return self.success_response(data, total=len(data))


class StatisticsMarketInsightsView(APIResponseMixin, APIView):
    """市场洞察（新增 - 综合分析）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取市场洞察数据"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(shop__icontains=search)
            )

        # 使用分析工具
        analytics = ProductAnalytics(queryset)
        data = analytics.get_market_insights()

        return self.success_response(data)


class StatisticsDashboardView(APIResponseMixin, APIView):
    """仪表板数据（新增 - 一次性获取所有关键指标）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取仪表板所需的所有关键数据"""
        queryset = Product.objects.all()

        # 应用筛选
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(shop__icontains=search)
            )

        # 使用分析工具
        analytics = ProductAnalytics(queryset)

        # 收集所有关键数据
        data = {
            'overview': analytics.get_overview(),
            'price_distribution': analytics.get_price_distribution(),
            'sales_distribution': analytics.get_sales_distribution(),
            'top_brands': analytics.get_brand_analysis(top_n=5),
            'top_regions': analytics.get_region_analysis(top_n=5),
            'top_shops': analytics.get_shop_analysis(top_n=5),
            'top_products_sales': analytics.get_top_products(top_n=5, sort_by='sales'),
            'top_products_price': analytics.get_top_products(top_n=5, sort_by='price'),
            'price_sales_correlation': analytics.get_price_sales_correlation(),
            'market_insights': analytics.get_market_insights(),
        }

        return self.success_response(data)
