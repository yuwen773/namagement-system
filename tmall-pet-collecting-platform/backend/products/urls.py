from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductExportView,
    ProductPriceHistoryView,
    CrawlLogListView,
    CrawlLogDetailView,
    StatisticsOverviewView,
    StatisticsPriceDistributionView,
    StatisticsTopSalesView,
    StatisticsShopRankingView,
    DataImportView,
    DataImportDetailView
)
from .statistics_views import (
    StatisticsOverviewView as StatisticsOverviewViewV2,
    StatisticsPriceDistributionView as StatisticsPriceDistributionViewV2,
    StatisticsSalesDistributionView,
    StatisticsBrandAnalysisView,
    StatisticsRegionAnalysisView,
    StatisticsShopAnalysisView,
    StatisticsTopProductsView,
    StatisticsPriceSalesCorrelationView,
    StatisticsAttributeAnalysisView,
    StatisticsBatchAnalysisView,
    StatisticsKeywordAnalysisView,
    StatisticsMarketInsightsView,
    StatisticsDashboardView,
    StatisticsPetTypeView,
    StatisticsPetUseView,
)

app_name = 'products'

urlpatterns = [
    # 商品管理
    path('export/', ProductExportView.as_view(), name='product_export'),
    path('', ProductListView.as_view(), name='product_list'),
    path('<uuid:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('<uuid:id>/price-history/', ProductPriceHistoryView.as_view(), name='price_history'),

    # 采集日志
    path('crawl-logs/', CrawlLogListView.as_view(), name='crawl_log_list'),
    path('crawl-logs/<uuid:id>/', CrawlLogDetailView.as_view(), name='crawl_log_detail'),

    # 数据导入
    path('import/', DataImportView.as_view(), name='data_import'),
    path('import/<str:task_id>/', DataImportDetailView.as_view(), name='data_import_detail'),

    # 数据统计 (优化版)
    path('statistics/overview/', StatisticsOverviewViewV2.as_view(), name='statistics_overview'),
    path('statistics/price-distribution/', StatisticsPriceDistributionViewV2.as_view(), name='price_distribution'),
    path('statistics/sales-distribution/', StatisticsSalesDistributionView.as_view(), name='sales_distribution'),
    path('statistics/brand-analysis/', StatisticsBrandAnalysisView.as_view(), name='brand_analysis'),
    path('statistics/region-analysis/', StatisticsRegionAnalysisView.as_view(), name='region_analysis'),
    path('statistics/shop-analysis/', StatisticsShopAnalysisView.as_view(), name='shop_analysis'),
    path('statistics/top-products/', StatisticsTopProductsView.as_view(), name='top_products'),
    path('statistics/price-sales-correlation/', StatisticsPriceSalesCorrelationView.as_view(), name='price_sales_correlation'),
    path('statistics/attribute-analysis/', StatisticsAttributeAnalysisView.as_view(), name='attribute_analysis'),
    path('statistics/batch-analysis/', StatisticsBatchAnalysisView.as_view(), name='batch_analysis'),
    path('statistics/keyword-analysis/', StatisticsKeywordAnalysisView.as_view(), name='keyword_analysis'),
    path('statistics/market-insights/', StatisticsMarketInsightsView.as_view(), name='market_insights'),
    path('statistics/dashboard/', StatisticsDashboardView.as_view(), name='dashboard'),
    path('statistics/pet-type/', StatisticsPetTypeView.as_view(), name='statistics-pet-type'),
    path('statistics/pet-use/', StatisticsPetUseView.as_view(), name='statistics-pet-use'),

    # 兼容旧接口
    path('statistics/top-sales/', StatisticsTopSalesView.as_view(), name='top_sales'),
    path('statistics/shop-ranking/', StatisticsShopRankingView.as_view(), name='shop_ranking'),
]
