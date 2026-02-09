from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count, Avg
from django.http import HttpResponse
import csv
from datetime import datetime

from .models import Product, CrawlLog, PriceHistory
from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductCreateSerializer,
    CrawlLogSerializer,
    CrawlLogCreateSerializer,
    PriceHistorySerializer
)
from users.permissions import IsAdminUser
from .services import ProductImportService


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


class ProductListView(APIResponseMixin, generics.ListCreateAPIView):
    """商品列表和创建"""
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer

    def list(self, request, *args, **kwargs):
        """获取商品列表，支持搜索和筛选"""
        queryset = self.get_queryset()

        # 搜索参数
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(shop__icontains=search) |
                Q(brand__icontains=search) |
                Q(tags__icontains=search)
            )

        # 价格区间筛选
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # 店铺筛选
        shop = request.query_params.get('shop')
        if shop:
            queryset = queryset.filter(shop__icontains=shop)

        # 品牌/类目筛选
        brand = request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)

        # 新增：地区筛选
        region = request.query_params.get('region')
        if region:
            queryset = queryset.filter(region__icontains=region)

        # 新增：标签筛选
        tags = request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags__icontains=tags)

        # 新增：批次号筛选
        batch_no = request.query_params.get('batch_no')
        if batch_no:
            queryset = queryset.filter(batch_no=batch_no)

        # 新增：商品ID筛选
        product_id = request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id__icontains=product_id)

        # 新增：排序选项支持
        ordering = request.query_params.get('ordering', '-crawl_time')
        # 验证排序字段是否安全
        valid_order_fields = [
            'crawl_time', '-crawl_time', 'price', '-price',
            'sales', '-sales', 'created_at', '-created_at',
            'updated_at', '-updated_at', 'title', '-title'
        ]
        if ordering in valid_order_fields:
            queryset = queryset.order_by(ordering)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        page_queryset = queryset[start:end]

        serializer = self.get_serializer(page_queryset, many=True)
        return self.success_response(serializer.data, total=total)

    def post(self, request, *args, **kwargs):
        """创建商品（仅管理员）"""
        if request.user.role != 'admin':
            return self.error_response("无权创建商品", code=403)

        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(serializer.data, "商品创建成功")
        return self.error_response(str(serializer.errors))


class ProductDetailView(APIResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    """商品详情、更新和删除"""
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """获取商品详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        """更新商品（仅管理员）"""
        if request.user.role != 'admin':
            return self.error_response("无权更新商品", code=403)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(serializer.data, "更新成功")
        return self.error_response(str(serializer.errors))

    def destroy(self, request, *args, **kwargs):
        """删除商品（仅管理员）"""
        if request.user.role != 'admin':
            return self.error_response("无权删除商品", code=403)

        instance = self.get_object()
        instance.delete()
        return self.success_response(message="删除成功")


class ProductExportView(APIResponseMixin, APIView):
    """商品数据导出（CSV格式）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """导出商品数据为CSV文件"""
        queryset = Product.objects.all()

        # 批次号筛选（用于导出最近采集的数据）
        batch_no = request.query_params.get('batch_no')
        if batch_no:
            queryset = queryset.filter(batch_no=batch_no)

        # 应用相同的筛选条件
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(shop__icontains=search) |
                Q(brand__icontains=search)
            )

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        shop = request.query_params.get('shop')
        if shop:
            queryset = queryset.filter(shop__icontains=shop)

        # 获取采集任务信息（如果有批次号）
        if batch_no:
            crawl_log = CrawlLog.objects.filter(
                log_content__contains=batch_no
            ).order_by('-created_at').first()
            keywords = crawl_log.keywords if crawl_log else ''
            filename_prefix = f"{keywords}_{batch_no}" if keywords else batch_no
        else:
            filename_prefix = "products_export"

        # 创建CSV响应
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            '商品ID', '商品标题', '价格', '价格单位', '价格描述',
            '销量', '店铺', '卖家昵称', '店铺标签',
            '地区', '商品标签', '图片URL', '详情页URL',
            '品牌', '类目', '批次号', '采集时间'
        ])

        for product in queryset:
            writer.writerow([
                str(product.id),
                product.title,
                str(product.price),
                product.price_unit or '',
                product.price_desc or '',
                str(product.sales),
                product.shop,
                product.seller_nick or '',
                product.shop_tags or '',
                product.region or '',
                product.tags or '',
                product.image_url or '',
                product.detail_url or '',
                product.brand or '',
                product.category or '',
                product.batch_no or '',
                product.crawl_time.strftime('%Y-%m-%d %H:%M:%S') if product.crawl_time else ''
            ])

        return response


class CrawlLogListView(APIResponseMixin, generics.ListCreateAPIView):
    """采集日志列表"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CrawlLogCreateSerializer
        return CrawlLogSerializer

    def get_queryset(self):
        return CrawlLog.objects.all()

    def list(self, request, *args, **kwargs):
        """获取采集日志列表"""
        # 状态筛选
        status_filter = request.query_params.get('status')
        queryset = self.get_queryset()
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        page_queryset = queryset[start:end]

        serializer = CrawlLogSerializer(page_queryset, many=True)
        return self.success_response(serializer.data, total=total)

    def post(self, request, *args, **kwargs):
        """创建采集日志（仅管理员）"""
        if request.user.role != 'admin':
            return self.error_response("无权创建日志", code=403)

        serializer = CrawlLogCreateSerializer(data=request.data)
        if serializer.is_valid():
            log = serializer.save()
            response_serializer = CrawlLogSerializer(log)
            return self.success_response(response_serializer.data, "日志创建成功")
        return self.error_response(str(serializer.errors))


class CrawlLogDetailView(APIResponseMixin, generics.RetrieveAPIView):
    """采集日志详情"""
    permission_classes = [IsAuthenticated]
    queryset = CrawlLog.objects.all()
    serializer_class = CrawlLogSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        """获取采集日志详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(serializer.data)


class StatisticsOverviewView(APIResponseMixin, APIView):
    """数据统计概览"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取统计概览数据"""
        total_products = Product.objects.count()
        total_shops = Product.objects.values('shop').distinct().count()
        avg_price = Product.objects.aggregate(avg=Avg('price'))['avg'] or 0
        total_sales = Product.objects.aggregate(total=Count('sales'))['total'] or 0

        data = {
            'total_products': total_products,
            'total_shops': total_shops,
            'avg_price': round(float(avg_price), 2),
            'total_sales': total_sales
        }
        return self.success_response(data)


class StatisticsPriceDistributionView(APIResponseMixin, APIView):
    """价格区间分布统计"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取价格区间分布"""
        ranges = [
            ('0-50', 0, 50),
            ('50-200', 50, 200),
            ('200-500', 200, 500),
            ('500+', 500, float('inf'))
        ]

        data = []
        for label, min_price, max_price in ranges:
            if max_price == float('inf'):
                count = Product.objects.filter(price__gte=min_price).count()
            else:
                count = Product.objects.filter(price__gte=min_price, price__lt=max_price).count()
            data.append({'range': label, 'count': count})

        return self.success_response(data)


class StatisticsTopSalesView(APIResponseMixin, APIView):
    """销量Top 10商品"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取销量最高的10个商品"""
        top_products = Product.objects.order_by('-sales')[:10]
        data = []
        for product in top_products:
            data.append({
                'id': str(product.id),
                'title': product.title,
                'price': str(product.price),
                'sales': product.sales,
                'shop': product.shop,
                'image_url': product.image_url
            })
        return self.success_response(data)


class StatisticsShopRankingView(APIResponseMixin, APIView):
    """店铺商品数量排行"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取店铺商品数量排行"""
        shops = Product.objects.values('shop').annotate(
            count=Count('id')
        ).order_by('-count')[:20]

        data = [{'shop': item['shop'], 'count': item['count']} for item in shops]
        return self.success_response(data)


class DataImportView(APIResponseMixin, APIView):
    """数据导入API - 启动和查询导入任务"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """启动数据导入任务"""
        try:
            # 获取自定义数据目录（可选）
            data_dir = request.data.get('data_dir')

            # 启动异步导入任务
            task_id = ProductImportService.start_import(data_dir)

            return self.success_response({
                'task_id': task_id,
                'message': '导入任务已启动'
            }, '数据导入任务已启动')

        except Exception as e:
            return self.error_response(f"启动导入任务失败: {str(e)}")

    def get(self, request):
        """获取所有导入任务状态"""
        tasks = ProductImportService.get_import_tasks()
        return self.success_response(tasks, total=len(tasks))


class DataImportDetailView(APIResponseMixin, APIView):
    """单个导入任务详情"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, task_id):
        """获取指定任务的状态"""
        task = ProductImportService.get_import_task(task_id)

        if not task:
            return self.error_response("任务不存在", code=404)

        return self.success_response(task)


class ProductPriceHistoryView(APIResponseMixin, APIView):
    """商品历史价格趋势查询"""
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """获取指定商品的历史价格趋势"""
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return self.error_response("商品不存在", code=404)

        # 获取该商品的历史价格记录，按日期升序排列
        price_history = PriceHistory.objects.filter(
            product=product
        ).order_by('record_date')

        # 获取查询参数
        days = request.query_params.get('days')
        if days:
            # 限制返回最近N天的记录（不包含今天）
            from datetime import timedelta
            from django.utils import timezone
            cutoff_date = (timezone.now().date() - timedelta(days=int(days) + 1))
            price_history = price_history.filter(record_date__gt=cutoff_date)

        data = []
        for record in price_history:
            data.append({
                'date': record.record_date.strftime('%Y-%m-%d'),
                'price': str(record.price),
                'sales': record.sales
            })

        # 如果没有历史记录，返回当前价格作为起点
        if not data:
            data.append({
                'date': product.crawl_time.strftime('%Y-%m-%d') if product.crawl_time else product.created_at.strftime('%Y-%m-%d'),
                'price': str(product.price),
                'sales': product.sales
            })

        return self.success_response(data)
