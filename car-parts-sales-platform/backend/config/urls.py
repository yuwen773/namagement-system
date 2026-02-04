"""
URL configuration for car_parts project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API 根视图 - 返回所有可用的 API 端点"""
    return Response({
        'message': '欢迎使用汽车改装件销售推荐平台 API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
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
    path('api/', api_root, name='api-root'),
    path('api/users/', include('apps.users.urls')),
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
