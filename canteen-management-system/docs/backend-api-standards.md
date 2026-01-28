# Django 后端开发规范

> 食堂管理系统后端开发规范文档
> 版本：v1.0
> 更新日期：2026-01-28

---

## 目录

1. [项目结构规范](#1-项目结构规范)
2. [接口响应格式规范](#2-接口响应格式规范)
3. [异常处理规范](#3-异常处理规范)
4. [分页查询规范](#4-分页查询规范)
5. [参数校验规范](#5-参数校验规范)
6. [序列化器开发规范](#6-序列化器开发规范)
7. [视图开发规范](#7-视图开发规范)
8. [路由规范](#8-路由规范)
9. [数据库操作规范](#9-数据库操作规范)
10. [代码风格规范](#10-代码风格规范)
11. [安全规范](#11-安全规范)

---

## 1. 项目结构规范

### 1.1 目录结构

```
backend/
├── config/                 # Django 项目配置
│   ├── settings.py        # 项目设置
│   ├── urls.py            # 主路由配置
│   └── wsgi.py
├── utils/                  # 公共工具模块
│   ├── __init__.py
│   ├── response.py        # 统一响应封装
│   ├── exceptions.py      # 自定义异常
│   ├── pagination.py      # 分页配置
│   └── constants.py       # 常量定义
├── accounts/              # 用户认证模块
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
├── employees/             # 员工档案模块
├── schedules/             # 排班管理模块
├── attendance/            # 考勤管理模块
├── leaves/                # 请假管理模块
├── salaries/              # 薪资管理模块
├── analytics/             # 数据统计模块
├── manage.py
└── requirements.txt
```

### 1.2 文件命名规范

| 文件类型 | 命名规范 | 示例 |
|---------|---------|------|
| 模块目录 | 小写单词 | `employees/` |
| Python 文件 | 小写下划线 | `employee_profile.py` |
| 模型类 | 大驼峰 | `EmployeeProfile` |
| 序列化器 | 大驼峰 + Serializer | `EmployeeProfileSerializer` |
| 视图 | 大驼峰 + ViewSet | `EmployeeProfileViewSet` |

---

## 2. 接口响应格式规范

### 2.1 统一响应结构

所有 API 接口必须返回统一的 JSON 格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        // 响应数据
    }
}
```

### 2.2 响应代码规范

| Code | HTTP Status | 说明 |
|------|-------------|------|
| 200 | 200 | 操作成功 |
| 201 | 201 | 创建成功 |
| 400 | 400 | 请求参数错误 |
| 401 | 401 | 未认证/认证失败 |
| 403 | 403 | 无权限 |
| 404 | 404 | 资源不存在 |
| 500 | 500 | 服务器内部错误 |

### 2.3 使用统一响应工具

**创建 `utils/response.py`：**

```python
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional


class ApiResponse:
    """统一响应封装类"""

    @staticmethod
    def success(data: Any = None, message: str = "操作成功", code: int = 200) -> Response:
        """
        成功响应

        Args:
            data: 响应数据
            message: 响应消息
            code: 业务状态码

        Returns:
            Response
        """
        return Response({
            'code': code,
            'message': message,
            'data': data
        }, status=status.HTTP_200_OK if code == 200 else status.HTTP_201_CREATED)

    @staticmethod
    def error(message: str, code: int = 400, errors: Optional[dict] = None, data: Any = None) -> Response:
        """
        错误响应

        Args:
            message: 错误消息
            code: 错误状态码
            errors: 详细错误信息
            data: 额外数据

        Returns:
            Response
        """
        response_data = {
            'code': code,
            'message': message,
            'data': data
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def paginate(data: dict, message: str = "获取成功") -> Response:
        """
        分页响应

        Args:
            data: 分页数据（包含 count, next, previous, results）
            message: 响应消息

        Returns:
            Response
        """
        return Response({
            'code': 200,
            'message': message,
            'data': data
        })
```

### 2.4 视图中使用示例

```python
from utils.response import ApiResponse

class EmployeeViewSet(viewsets.ModelViewSet):
    """员工档案视图集"""

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取员工列表成功')

    def retrieve(self, request, *args, **kwargs):
        """详情查询"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取员工详情成功')

    def create(self, request, *args, **kwargs):
        """创建"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='创建成功', code=201)
        return ApiResponse.error(message='创建失败', errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """更新"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='更新成功')
        return ApiResponse.error(message='更新失败', errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """删除"""
        instance = self.get_object()
        instance.delete()
        return ApiResponse.success(message='删除成功')
```

---

## 3. 异常处理规范

### 3.1 自定义异常类

**创建 `utils/exceptions.py`：**

```python
from rest_framework.exceptions import APIException


class BusinessError(APIException):
    """
    业务异常基类

    用于处理业务逻辑中的错误，如数据验证失败、状态不允许等
    """
    status_code = 400
    default_detail = '业务处理失败'
    default_code = 'business_error'

    def __init__(self, detail: str = None, code: int = 400):
        """
        Args:
            detail: 错误详情
            code: 业务状态码
        """
        self.detail = detail or self.default_detail
        self.code = code


class ValidationError(BusinessError):
    """参数验证异常"""
    default_detail = '参数验证失败'


class NotFoundError(BusinessError):
    """资源不存在异常"""
    status_code = 404
    default_detail = '资源不存在'


class PermissionDeniedError(BusinessError):
    """权限不足异常"""
    status_code = 403
    default_detail = '权限不足'


class StateNotAllowedError(BusinessError):
    """状态不允许异常"""
    default_detail = '当前状态不允许此操作'
```

### 3.2 全局异常处理器

**创建 `utils/handlers.py`：**

```python
from rest_framework.views import exception_handler
from rest_framework import status
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    自定义全局异常处理器

    Args:
        exc: 异常对象
        context: 上下文信息

    Returns:
        Response 或 None
    """
    # 调用 DRF 默认异常处理
    response = exception_handler(exc, context)

    if response is not None:
        # 处理 DRF 异常
        if isinstance(exc, DatabaseError):
            logger.error(f"数据库错误: {str(exc)}")
            return Response({
                'code': 500,
                'message': '数据操作失败',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 格式化 DRF 异常响应
        custom_response_data = {
            'code': response.status_code,
            'message': get_error_message(exc),
            'data': None
        }
        if hasattr(exc, 'detail') and isinstance(exc.detail, dict):
            custom_response_data['errors'] = exc.detail

        response.data = custom_response_data
        return response

    # 处理未捕获的异常
    logger.error(f"未捕获的异常: {str(exc)}", exc_info=True)
    return Response({
        'code': 500,
        'message': '服务器内部错误',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_error_message(exc):
    """获取友好的错误消息"""
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, str):
            return exc.detail
        elif isinstance(exc.detail, dict):
            return list(exc.detail.values())[0][0] if exc.detail else '请求参数错误'
    return str(exc)
```

### 3.3 在 settings.py 中配置

```python
# config/settings.py

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.handlers.custom_exception_handler',
    # 其他配置...
}
```

### 3.4 在视图中使用自定义异常

```python
from utils.exceptions import BusinessError, StateNotAllowedError
from utils.response import ApiResponse

class LeaveRequestViewSet(viewsets.ModelViewSet):
    """请假申请视图集"""

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """审批请假"""
        leave_request = self.get_object()

        # 检查状态
        if leave_request.status != LeaveRequest.Status.PENDING:
            raise StateNotAllowedError(
                detail=f'该请假申请已被{leave_request.get_status_display()}，无法重复操作'
            )

        # 业务逻辑...
        return ApiResponse.success(data=serializer.data, message='审批成功')
```

---

## 4. 分页查询规范

### 4.1 全局分页配置

**在 `settings.py` 中配置：**

```python
# config/settings.py

REST_FRAMEWORK = {
    # 分页配置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100,
}
```

### 4.2 自定义分页类

**创建 `utils/pagination.py`：**

```python
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """标准分页类"""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        返回统一格式的分页响应

        配合 ApiResponse 使用时，返回 data 字典内容
        """
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }
```

### 4.3 视图中使用分页

```python
from utils.pagination import StandardPagination
from utils.response import ApiResponse

class EmployeeViewSet(viewsets.ModelViewSet):
    """员工档案视图集"""
    pagination_class = StandardPagination

    def list(self, request, *args, **kwargs):
        """列表查询（自动分页）"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)
```

### 4.4 分页查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| page_size | int | 20 | 每页数量（最大100） |

### 4.5 查询条件规范

列表查询接口应支持的查询条件：

1. **精确匹配**：使用 `filterset_fields`
2. **模糊搜索**：使用 `search_fields`
3. **范围筛选**：自定义 filter
4. **排序**：使用 `ordering_fields`

```python
class EmployeeViewSet(viewsets.ModelViewSet):
    """员工档案视图集"""
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 精确匹配字段
    filterset_fields = {
        'position': ['exact'],           # 岗位精确匹配
        'status': ['exact'],             # 状态精确匹配
        'entry_date': ['gte', 'lte'],    # 入职日期范围
        'created_at': ['gte', 'lte'],    # 创建时间范围
    }

    # 模糊搜索字段
    search_fields = ['name', 'phone', 'id_card']

    # 排序字段
    ordering_fields = ['created_at', 'entry_date', 'name']
    ordering = ['-created_at']
```

---

## 5. 参数校验规范

### 5.1 序列化器校验

所有接口请求参数必须通过 Serializer 进行校验：

```python
from rest_framework import serializers


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """员工创建序列化器"""

    # 基础字段校验
    name = serializers.CharField(
        max_length=50,
        required=True,
        error_messages={'required': '姓名不能为空', 'blank': '姓名不能为空'}
    )

    phone = serializers.CharField(
        max_length=20,
        required=True,
        error_messages={'required': '手机号不能为空'}
    )

    id_card = serializers.CharField(
        max_length=18,
        required=True,
        error_messages={'required': '身份证号不能为空'}
    )

    class Meta:
        model = EmployeeProfile
        fields = ['name', 'phone', 'id_card', 'position', 'entry_date']

    # 自定义字段校验
    def validate_phone(self, value):
        """校验手机号格式"""
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        return value

    def validate_id_card(self, value):
        """校验身份证号格式"""
        import re
        if not re.match(r'^\d{17}[\dXx]$', value):
            raise serializers.ValidationError('身份证号格式不正确')
        return value

    # 联合字段校验
    def validate(self, attrs):
        """联合校验"""
        entry_date = attrs.get('entry_date')
        if entry_date and entry_date > date.today():
            raise serializers.ValidationError('入职日期不能晚于今天')
        return attrs
```

### 5.2 视图中使用序列化器校验

```python
def create(self, request, *args, **kwargs):
    """创建"""
    serializer = EmployeeCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return ApiResponse.success(data=serializer.data, message='创建成功', code=201)

    # 校验失败，返回详细错误信息
    return ApiResponse.error(
        message='参数验证失败',
        errors=serializer.errors
    )
```

### 5.3 必须校验的参数类型

| 参数类型 | 校验规则 | 示例 |
|---------|---------|------|
| 手机号 | 正则校验 | `^1[3-9]\d{9}$` |
| 身份证 | 正则校验 | `^\d{17}[\dXx]$` |
| 邮箱 | EmailField | `EmailField` |
| 日期 | 日期格式 + 合理性 | 不能晚于今天 |
| 金额 | DecimalField | 精度控制 |
| 枚举 | ChoiceField | 只允许指定值 |

---

## 6. 序列化器开发规范

### 6.1 序列化器命名

| 类型 | 命名规范 | 示例 |
|------|---------|------|
| 基础序列化器 | 模型名 + Serializer | `EmployeeSerializer` |
| 列表序列化器 | 模型名 + ListSerializer | `EmployeeListSerializer` |
| 创建序列化器 | 模型名 + CreateSerializer | `EmployeeCreateSerializer` |
| 更新序列化器 | 模型名 + UpdateSerializer | `EmployeeUpdateSerializer` |
| 操作序列化器 | 操作名 + Serializer | `ApproveSerializer` |

### 6.2 序列化器字段规范

```python
class EmployeeListSerializer(serializers.ModelSerializer):
    """员工列表序列化器（简化版）"""

    # 添加显示字段
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'name', 'phone', 'position', 'position_display',
            'status', 'status_display', 'entry_date'
        ]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """员工详情序列化器（完整版）"""

    # 关联字段
    department_name = serializers.CharField(source='department.name', read_only=True)

    # 计算字段
    work_years = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeProfile
        fields = '__all__'  # 或明确列出所有字段
        extra_kwargs = {
            'id_card': {'write_only': True},  # 敏感字段只写
        }

    def get_work_years(self, obj):
        """计算工作年限"""
        if obj.entry_date:
            return (date.today() - obj.entry_date).days // 365
        return 0
```

### 6.3 嵌套序列化器

```python
class ScheduleSerializer(serializers.ModelSerializer):
    """排班序列化器（含嵌套）"""

    # 嵌套序列化
    employee = EmployeeListSerializer(read_only=True)
    shift = ShiftListSerializer(read_only=True)

    # 写入时使用 ID
    employee_id = serializers.IntegerField(write_only=True)
    shift_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'employee', 'shift', 'employee_id', 'shift_id', 'work_date']
```

---

## 7. 视图开发规范

### 7.1 ViewSet 基础规范

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from utils.response import ApiResponse
from utils.pagination import StandardPagination
from utils.exceptions import BusinessError


class BaseModelViewSet(viewsets.ModelViewSet):
    """基础视图集（封装通用逻辑）"""

    pagination_class = StandardPagination

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return self.serializer_list_class
        if self.action == 'create':
            return self.serializer_create_class
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """详情查询"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='创建成功', code=201)
        return ApiResponse.error(message='创建失败', errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """更新"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='更新成功')
        return ApiResponse.error(message='更新失败', errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """删除"""
        instance = self.get_object()
        instance.delete()
        return ApiResponse.success(message='删除成功')
```

### 7.2 自定义 Action 规范

```python
class LeaveRequestViewSet(viewsets.ModelViewSet):
    """请假申请视图集"""

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        审批请假

        请求参数：
        - approve: True(批准) / False(拒绝)
        - approval_remark: 审批备注
        """
        leave_request = self.get_object()

        # 状态检查
        if leave_request.status != LeaveRequest.Status.PENDING:
            raise BusinessError(
                detail=f'该请假申请已被{leave_request.get_status_display()}，无法重复操作'
            )

        # 参数校验
        serializer = LeaveApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 业务逻辑
        approve = serializer.validated_data['approve']
        leave_request.status = (
            LeaveRequest.Status.APPROVED if approve else LeaveRequest.Status.REJECTED
        )
        leave_request.approval_remark = serializer.validated_data.get('approval_remark', '')
        leave_request.save()

        return ApiResponse.success(
            data=LeaveRequestSerializer(leave_request).data,
            message='审批成功'
        )

    @action(detail=False, methods=['get'], url_path='my-requests')
    def my_requests(self, request):
        """
        我的请假申请

        查询参数：
        - employee_id: 员工ID（必填）
        - status: 状态筛选（可选）
        """
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return ApiResponse.error(message='缺少 employee_id 参数')

        queryset = self.queryset.filter(employee_id=employee_id)

        # 可选筛选
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        queryset = queryset.order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)

        return ApiResponse.success(data=serializer.data)
```

### 7.3 文档字符串规范

每个视图类和方法必须有文档字符串：

```python
class EmployeeViewSet(viewsets.ModelViewSet):
    """
    员工档案视图集

    提供员工档案的 CRUD 操作：
    - list: 获取员工列表
    - retrieve: 获取员工详情
    - create: 创建员工档案
    - update: 更新员工档案
    - destroy: 删除员工档案
    """

    @action(detail=False, methods=['get'])
    def by_position(self, request):
        """
        按岗位查询员工

        查询参数：
        - position: 岗位代码（必填）CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER

        返回：
        - 指定岗位的员工列表
        """
        pass
```

---

## 8. 路由规范

### 8.1 路由命名规范

```
api/{module}/{resource}/{action}

示例：
/api/employees/                    # 员工列表
/api/employees/{id}/               # 员工详情
/api/employees/{id}/activate/      # 激活员工
/api/leaves/my-requests/           # 我的请假申请
/api/leaves/{id}/approve/          # 审批请假
```

### 8.2 路由配置

```python
# employees/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 8.3 主路由配置

```python
# config/urls.py

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/employees/", include("employees.urls")),
    path("api/schedules/", include("schedules.urls")),
    path("api/attendance/", include("attendance.urls")),
    path("api/leaves/", include("leaves.urls")),
    path("api/salaries/", include("salaries.urls")),
    path("api/analytics/", include("analytics.urls")),
]
```

**注意：**
- 所有 API 路由必须有 `/api/` 前缀
- 模块名使用复数形式（employees、leaves）
- 自定义 action 使用 kebab-case 命名（my-requests、approve）

---

## 9. 数据库操作规范

### 9.1 查询优化

```python
# 使用 select_related 减少 SQL 查询（ForeignKey）
queryset = Schedule.objects.select_related('employee', 'shift')

# 使用 prefetch_related 减少 SQL 查询（ManyToMany）
queryset = Employee.objects.prefetch_related('schedules')

# 只查询需要的字段
queryset = Employee.objects.only('id', 'name', 'phone')

# 排除某些字段
queryset = Employee.objects.defer('id_card', 'address')
```

### 9.2 事务处理

```python
from django.db import transaction

@transaction.atomic
def complex_operation():
    """复杂操作使用事务"""
    try:
        # 多个数据库操作
        employee = Employee.objects.create(...)
        Schedule.objects.create(employee=employee, ...)
    except Exception as e:
        transaction.set_rollback(True)
        raise
```

### 9.3 批量操作

```python
# 批量创建
Schedule.objects.bulk_create([
    Schedule(employee_id=eid, work_date=date, shift_id=sid)
    for eid in employee_ids
    for date in date_range
])

# 批量更新
Schedule.objects.filter(work_date__gte=start).update(is_swapped=True)

# 批量删除
Schedule.objects.filter(work_date__lt=end).delete()
```

---

## 10. 代码风格规范

### 10.1 导入顺序

```python
# 1. 标准库导入
from datetime import datetime, timedelta
from decimal import Decimal

# 2. 第三方库导入
from rest_framework import viewsets, status
from django.db.models import Q, Sum

# 3. 本地应用导入
from .models import EmployeeProfile
from .serializers import EmployeeSerializer
from utils.response import ApiResponse
```

### 10.2 命名规范

```python
# 类名：大驼峰
class EmployeeProfileViewSet:
    pass

# 函数/方法名：小写下划线
def get_employee_list():
    pass

# 变量名：小写下划线
employee_list = []
page_size = 20

# 常量：大写下划线
DEFAULT_PAGE_SIZE = 20
MAX_RETRY_COUNT = 3
```

### 10.3 注释规范

```python
def calculate_overtime_pay(overtime_hours, base_salary):
    """
    计算加班费

    Args:
        overtime_hours (float): 加班小时数
        base_salary (Decimal): 基本工资

    Returns:
        Decimal: 加班费金额

    计算公式：
    日工资 = 月工资 / 21.75
    时薪 = 日工资 / 8
    加班费 = 时薪 * 1.5 * 加班小时数
    """
    daily_salary = base_salary / Decimal('21.75')
    hourly_salary = daily_salary / Decimal('8')
    return hourly_salary * Decimal('1.5') * Decimal(str(overtime_hours))
```

---

## 11. 安全规范

### 11.1 密码处理

```python
# 生产环境必须加密密码
from django.contrib.auth.hash import make_password

user = User.objects.create(
    username='admin',
    password=make_password('admin123')  # 加密存储
)
```

### 11.2 敏感数据处理

```python
class EmployeeSerializer(serializers.ModelSerializer):
    """员工序列化器"""

    class Meta:
        model = EmployeeProfile
        fields = ['id', 'name', 'phone', 'id_card', 'salary']
        extra_kwargs = {
            'id_card': {'write_only': True},      # 身份证号只写
            'salary': {'write_only': True},       # 薪资只写
        }
```

### 11.3 SQL 注入防护

```python
# 正确：使用 ORM 参数化查询
Employee.objects.filter(name=user_input)

# 错误：直接拼接 SQL（禁止！）
# Employee.objects.raw(f"SELECT * FROM employees WHERE name = '{user_input}'")
```

### 11.4 权限控制

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class EmployeeViewSet(viewsets.ModelViewSet):
    """员工档案视图集"""

    # 列表和详情：登录即可访问
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
```

---

## 附录

### A. 常用代码片段

**ViewSet 基础模板：**

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from utils.response import ApiResponse
from utils.pagination import StandardPagination

class ExampleViewSet(viewsets.ModelViewSet):
    """示例视图集"""

    pagination_class = StandardPagination

    def get_queryset(self):
        """获取查询集"""
        return Example.objects.all()

    def get_serializer_class(self):
        """获取序列化器"""
        if self.action == 'list':
            return ExampleListSerializer
        return ExampleSerializer
```

**分页响应模板：**

```python
def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    page = self.paginate_queryset(queryset)

    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

    serializer = self.get_serializer(queryset, many=True)
    return ApiResponse.success(data=serializer.data)
```

### B. 快速检查清单

开发完成后，检查以下项目：

- [ ] 所有接口使用 `ApiResponse` 返回
- [ ] 所有参数通过 Serializer 校验
- [ ] 列表接口支持分页
- [ ] 错误信息清晰易懂
- [ ] 文档字符串完整
- [ ] 敏感字段标记为 write_only
- [ ] 查询使用了 select_related/prefetch_related
- [ ] 路由命名符合规范
- [ ] 代码符合 PEP 8 规范

---

**文档维护：** 本规范应随着项目发展持续更新。
**问题反馈：** 发现规范问题请在团队会议中提出讨论。
