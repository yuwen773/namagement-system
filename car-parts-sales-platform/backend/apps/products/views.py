from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
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
    permission_classes = [AllowAny]  # 允许匿名查看分类
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['sort_order', 'id']

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('tree') == 'true':
            return CategoryTreeSerializer
        return CategorySerializer

    def list(self, request, *args, **kwargs):
        """获取分类列表"""
        queryset = self.filter_queryset(self.get_queryset())
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
    permission_classes = [AllowAny]  # 允许匿名浏览商品
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def list(self, request, *args, **kwargs):
        """获取商品列表"""
        queryset = self.filter_queryset(self.get_queryset())
        # Temporarily disable pagination for debugging
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取商品详情"""
        instance = self.get_object()
        # 增加浏览量
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
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
                # 获取分页响应字典而不是 Response 对象
                paginated_data = self.get_paginated_response(serializer.data)
                # 如果是 Response 对象则获取 data 属性
                if hasattr(paginated_data, 'data'):
                    paginated_data = paginated_data.data
                return ApiResponse.paginate(data=paginated_data)

            serializer = ReviewListSerializer(reviews, many=True)
            return ApiResponse.success(data=serializer.data)
        else:
            # 提交评价
            product = self.get_object()
            user_id = request.user.id if request.user.is_authenticated else 1

            create_data = {
                'rating': request.data.get('rating', 5),
                'comment': request.data.get('comment', ''),
                'images': request.data.get('images', []),
                'is_anonymous': request.data.get('is_anonymous', False),
                'order_item_id': request.data.get('order_item_id'),
            }

            serializer = ReviewCreateSerializer(data=create_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product, user_id=user_id)

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
    permission_classes = [AllowAny]  # 允许匿名查看图片
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

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
    permission_classes = [AllowAny]  # 允许匿名查看属性
    serializer_class = ProductAttributeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

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
    permission_classes = [AllowAny]  # 允许匿名查看评价
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

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
        # 从URL获取商品ID
        product_id = kwargs.get('product_id')
        if not product_id:
            return ApiResponse.error(message='商品ID不能为空', code=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return ApiResponse.error(message='商品不存在', code=404)

        # 获取当前用户ID（如果未登录则使用默认ID）
        user_id = request.user.id if request.user.is_authenticated else 1

        # 准备创建数据
        create_data = {
            'rating': request.data.get('rating', 5),
            'comment': request.data.get('comment', ''),
            'images': request.data.get('images', []),
            'is_anonymous': request.data.get('is_anonymous', False),
            'order_item_id': request.data.get('order_item_id'),
        }

        serializer = ReviewCreateSerializer(data=create_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product, user_id=user_id)

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
