from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from utils.response import ApiResponse
from .models import Category, Product, ProductImage, ProductAttribute, Review
from .serializers import (
    CategorySerializer, CategoryTreeSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ProductImageSerializer, ProductAttributeSerializer,
    ReviewSerializer, ReviewCreateSerializer, ReviewListSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    商品分类管理 ViewSet

    list: 获取分类列表（树形结构）
    retrieve: 获取单个分类详情
    create: 创建分类
    update: 更新分类
    partial_update: 部分更新
    destroy: 删除分类
    """
    queryset = Category.objects.filter(is_active=True)
    permission_classes = [AllowAny]  # 默认允许匿名查看
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['sort_order', 'id']

    def get_permissions(self):
        """
        获取权限配置
        - 列表和详情：允许匿名访问
        - 创建、更新、删除：需要管理员权限
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('tree') == 'true':
            return CategoryTreeSerializer
        return CategorySerializer

    def list(self, request, *args, **kwargs):
        """获取分类列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取分类详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建分类"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新分类"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除分类"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取完整分类树"""
        # 获取所有顶级分类及其子分类
        categories = Category.objects.filter(parent__isnull=True, is_active=True)
        serializer = CategoryTreeSerializer(categories, many=True)
        return ApiResponse.success(data=serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    商品管理 ViewSet

    list: 获取商品列表
    retrieve: 获取商品详情
    create: 创建商品（管理员）
    update: 更新商品（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除商品（管理员）
    """
    queryset = Product.objects.all()
    permission_classes = [AllowAny]  # 默认允许匿名浏览
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        'category': ['exact', 'in'],
        'price': ['gte', 'lte'],
        'status': ['exact'],
        'is_featured': ['exact'],
        'is_new': ['exact'],
    }
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'price', 'sales_count', 'view_count']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        获取权限配置
        - 列表和详情：允许匿名访问
        - 创建、更新、删除、发布、下架：需要管理员权限
        - 评价：需要登录（在 action 中单独处理）
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish', 'archive']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def list(self, request, *args, **kwargs):
        """获取商品列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取商品详情"""
        instance = self.get_object()
        # 增加浏览量（使用 F 表达式避免竞态条件）
        Product.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db()  # 刷新获取最新数据
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建商品"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新商品"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除商品"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布商品"""
        product = self.get_object()
        product.status = 'published'
        product.save(update_fields=['status', 'updated_at'])
        return ApiResponse.success(message='发布成功', data=ProductDetailSerializer(product).data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """下架商品"""
        product = self.get_object()
        product.status = 'archived'
        product.save(update_fields=['status', 'updated_at'])
        return ApiResponse.success(message='下架成功', data=ProductDetailSerializer(product).data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """获取推荐商品"""
        products = Product.objects.filter(status='published', is_featured=True)
        queryset = self.filter_queryset(products)
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    @action(detail=False, methods=['get'], url_path='new-arrivals')
    def new_arrivals(self, request):
        """获取新品上市"""
        products = Product.objects.filter(status='published', is_new=True)
        queryset = self.filter_queryset(products)
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def reviews(self, request, pk=None):
        """
        获取或提交商品评价

        GET: 获取指定商品的评价列表
        POST: 为指定商品提交评价

        URL: /api/products/products/{id}/reviews/
        """
        if request.method == 'GET':
            # 获取评价列表
            product = self.get_object()
            reviews = Review.objects.filter(product=product).order_by('-created_at')

            # 支持评分筛选
            rating = request.query_params.get('rating')
            if rating:
                reviews = reviews.filter(rating=rating)

            # 支持排序
            ordering = request.query_params.get('ordering', '-created_at')
            if ordering in ['created_at', '-created_at', 'rating', '-rating']:
                reviews = reviews.order_by(ordering)

            # 分页
            page = self.paginate_queryset(reviews)
            if page is not None:
                serializer = ReviewListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = ReviewListSerializer(reviews, many=True)
            return ApiResponse.success(data=serializer.data)
        else:
            # 提交评价
            if not request.user.is_authenticated:
                return ApiResponse.error(message='请先登录', code=401)

            product = self.get_object()
            order_item_id = request.data.get('order_item_id')

            # 验证订单项（如果提供）
            if order_item_id:
                from apps.orders.models import OrderItem, Order

                try:
                    order_item = OrderItem.objects.select_related('order').get(id=order_item_id)
                    order = order_item.order

                    # 验证订单所有者
                    if order.user_id != request.user.id:
                        return ApiResponse.error(message='只能评价自己的订单', code=403)

                    # 验证订单状态
                    if order.status != Order.Status.COMPLETED:
                        return ApiResponse.error(message='只有已完成的订单才能评价')

                    # 验证商品是否匹配
                    if order_item.product_id != product.id:
                        return ApiResponse.error(message='订单商品与评价商品不匹配')

                except OrderItem.DoesNotExist:
                    return ApiResponse.error(message='订单项不存在', code=404)

            create_data = {
                'rating': request.data.get('rating', 5),
                'comment': request.data.get('comment', ''),
                'images': request.data.get('images', []),
                'is_anonymous': request.data.get('is_anonymous', False),
                'order_item_id': order_item_id,
            }

            serializer = ReviewCreateSerializer(data=create_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product, user_id=request.user.id)

            # 返回完整评价信息
            review = Review.objects.get(id=serializer.instance.id)
            return ApiResponse.success(
                message='评价提交成功',
                data=ReviewSerializer(review).data,
                code=201
            )


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    商品图片管理 ViewSet
    """
    queryset = ProductImage.objects.all()
    permission_classes = [AllowAny]  # 默认允许匿名查看
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

    def get_permissions(self):
        """
        获取权限配置
        - 列表：允许匿名访问
        - 创建、删除：需要管理员权限
        """
        if self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    商品属性管理 ViewSet
    """
    queryset = ProductAttribute.objects.all()
    permission_classes = [AllowAny]  # 默认允许匿名查看
    serializer_class = ProductAttributeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

    def get_permissions(self):
        """
        获取权限配置
        - 列表：允许匿名访问
        - 创建、删除：需要管理员权限
        """
        if self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')


class ReviewViewSet(viewsets.ModelViewSet):
    """
    商品评价 ViewSet

    提供以下接口：
    - GET /api/products/reviews/ - 获取评价列表
    - GET /api/products/reviews/{id}/ - 获取评价详情
    - POST /api/products/products/{product_id}/reviews/ - 提交评价
    - GET /api/products/products/{product_id}/reviews/ - 获取商品评价列表
    """
    queryset = Review.objects.all()
    permission_classes = [AllowAny]  # 默认允许匿名查看
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        获取权限配置
        - 列表和详情：允许匿名访问
        - 删除：需要管理员权限
        - 创建：需要登录（在 action 中单独处理，这里也可以加 IsAuthenticated）
        """
        if self.action == 'destroy':
            return [IsAdminUser()]
        # create 权限在 action 内部有逻辑判断，但最好也在 level 上限制
        # 注意：由于 create 逻辑在 ReviewViewSet.create 中手动实现了登录检查，这里暂不强制 IsAuthenticated，
        # 或者可以加上。
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewSerializer

    def list(self, request, *args, **kwargs):
        """获取评价列表"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取评价详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """
        提交商品评价

        请求参数：
        - product_id: 商品ID（URL中）
        - rating: 评分（1-5）
        - comment: 评价内容
        - images: 评价图片列表
        - is_anonymous: 是否匿名
        - order_item_id: 订单项ID（可选）
        """
        # 验证用户登录
        if not request.user.is_authenticated:
            return ApiResponse.error(message='请先登录', code=401)

        # 从URL获取商品ID
        product_id = kwargs.get('product_id')
        if not product_id:
            return ApiResponse.error(message='商品ID不能为空', code=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return ApiResponse.error(message='商品不存在', code=404)

        order_item_id = request.data.get('order_item_id')

        # 验证订单项（如果提供）
        if order_item_id:
            from apps.orders.models import OrderItem, Order

            try:
                order_item = OrderItem.objects.select_related('order').get(id=order_item_id)
                order = order_item.order

                # 验证订单所有者
                if order.user_id != request.user.id:
                    return ApiResponse.error(message='只能评价自己的订单', code=403)

                # 验证订单状态
                if order.status != Order.Status.COMPLETED:
                    return ApiResponse.error(message='只有已完成的订单才能评价')

                # 验证商品是否匹配
                if order_item.product_id != product.id:
                    return ApiResponse.error(message='订单商品与评价商品不匹配')

            except OrderItem.DoesNotExist:
                return ApiResponse.error(message='订单项不存在', code=404)

        # 准备创建数据
        create_data = {
            'rating': request.data.get('rating', 5),
            'comment': request.data.get('comment', ''),
            'images': request.data.get('images', []),
            'is_anonymous': request.data.get('is_anonymous', False),
            'order_item_id': order_item_id,
        }

        serializer = ReviewCreateSerializer(data=create_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, user_id=request.user.id)

        # 返回完整评价信息
        review = Review.objects.get(id=serializer.instance.id)
        return ApiResponse.success(
            message='评价提交成功',
            data=ReviewSerializer(review).data,
            code=201
        )

    def destroy(self, request, *args, **kwargs):
        """删除评价（管理员）"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')

    @action(detail=False, methods=['get'], url_path='me')
    def my_reviews(self, request):
        """
        获取当前登录用户的评价列表

        URL: GET /api/products/reviews/me/
        描述: 获取当前登录用户发表的所有评价记录
        """
        # 验证用户登录
        if not request.user.is_authenticated:
            return ApiResponse.error(message='请先登录', code=401)

        # 获取当前用户的评价
        reviews = Review.objects.filter(user_id=request.user.id).order_by('-created_at')

        # 支持评分筛选
        rating = request.query_params.get('rating')
        if rating:
            try:
                reviews = reviews.filter(rating=int(rating))
            except (ValueError, TypeError):
                pass

        # 支持排序
        ordering = request.query_params.get('ordering', '-created_at')
        valid_orderings = ['created_at', '-created_at', 'rating', '-rating']
        if ordering in valid_orderings:
            reviews = reviews.order_by(ordering)

        # 分页
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(reviews, many=True)
        return ApiResponse.success(data=serializer.data)
