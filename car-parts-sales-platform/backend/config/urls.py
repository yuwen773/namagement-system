"""
URL configuration for car_parts project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Swagger/OpenAPI 配置
schema_view = get_schema_view(
    openapi.Info(
        title='汽车改装件销售推荐平台 API',
        default_version='v1.0',
        description='''汽车改装件销售推荐平台 RESTful API 文档

## 功能模块
- **用户管理**: 用户注册、登录、个人信息、收货地址
- **商品管理**: 商品分类、商品列表、商品详情、商品评价
- **订单管理**: 购物车、订单创建、订单列表、订单详情、退换货
- **营销管理**: 优惠券领取、我的优惠券
- **推荐管理**: 热门推荐、新品推荐、个性化推荐
- **内容管理**: 改装案例、常见问题
- **系统管理**: 系统配置、站内消息、操作日志

## 认证方式
本 API 使用 JWT (JSON Web Token) 进行身份认证。

### 获取 Token
1. **注册**: `POST /api/auth/register/`
2. **登录**: `POST /api/auth/login/`

### 使用 Token
在请求头中添加:
```
Authorization: Bearer <your_access_token>
```

## 统一响应格式
所有 API 返回格式:
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {...}
}
```

分页响应格式:
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "page": 1,
        "page_size": 20,
        "results": [...]
    }
}
```
''',
        terms_of_service='https://www.example.com/terms/',
        contact=openapi.Contact(email='support@example.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API 根视图 - 返回所有可用的 API 端点"""
    return Response({
        'message': '欢迎使用汽车改装件销售推荐平台 API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'swagger': '/swagger/',
            'redoc': '/redoc/',
            'users': '/api/users/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'marketing': '/api/marketing/',
            'recommendations': '/api/recommendations/',
            'content': '/api/content/',
            'system': '/api/system/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    # API 文档
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # API 端点
    path('api/', api_root, name='api-root'),
    path('api/auth/', include('apps.users.auth_urls')),  # 认证接口：注册、登录、获取用户信息
    path('api/users/', include('apps.users.urls')),  # 用户管理接口
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/marketing/', include('apps.marketing.urls')),
    path('api/recommendations/', include('apps.recommendations.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/system/', include('apps.system.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
