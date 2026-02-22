# 后端接口参数校验与异常处理规范实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 统一后端接口的参数校验和异常处理，建立详细的业务错误码体系，便于前端精确处理不同错误类型。

**Architecture:** 增强现有的 `utils/exceptions.py` 异常类体系，添加错误码支持；优化 `utils/handlers.py` 全局异常处理器，支持新的错误码格式；改造视图层使用统一的异常抛出方式。

**Tech Stack:** Django 5.2 + Django REST Framework + Python

---

## 实施步骤概览

1. Task 1-2: 增强 `utils/exceptions.py` - 添加错误码和新的异常类体系
2. Task 3-4: 优化 `utils/handlers.py` - 支持新的错误码格式响应
5. Task 5-8: 改造 `accounts/views.py` - 使用新的异常类
9. Task 9-12: 改造 `employees/views.py` - 使用新的异常类
13. Task 13-16: 改造 `schedules/views.py` - 使用新的异常类
17. Task 17-20: 改造 `leaves/views.py` - 使用新的异常类
21. Task 21-24: 改造 `attendance/views.py` - 使用新的异常类
25. Task 28-28: 改造 `salaries/views.py` - 使用新的异常类

---

## Task 1: 创建带错误码的异常基类

**Files:**
- Modify: `backend/utils/exceptions.py`

**Step 1: 查看现有异常类**

```bash
cat backend/utils/exceptions.py
```

**Step 2: 添加新的异常基类**

在 `backend/utils/exceptions.py` 文件末尾添加：

```python
class BaseAPIException(APIException):
    """API 异常基类，带错误码支持"""
    status_code = 400
    error_code = 'E100'
    default_message = '操作失败'

    def __init__(self, message=None, detail=None):
        self.detail = message or self.default_message
        super().__init__(detail=self.detail)

    @property
    def error_code_value(self):
        return self.error_code
```

**Step 3: 验证语法正确性**

```bash
cd backend && python -c "from utils.exceptions import BaseAPIException; print('OK')"
```

---

## Task 2: 添加所有业务异常类

**Files:**
- Modify: `backend/utils/exceptions.py`

**Step 1: 添加参数验证异常类**

在 `BaseAPIException` 后添加：

```python
class ValidationException(BaseAPIException):
    """参数验证失败异常"""
    status_code = 400
    error_code = 'E100'
    default_message = '参数验证失败'


class RequiredFieldException(BaseAPIException):
    """缺少必需参数异常"""
    status_code = 400
    error_code = 'E101'
    default_message = '缺少必需参数'


class FormatErrorException(BaseAPIException):
    """参数格式错误异常"""
    status_code = 400
    error_code = 'E102'
    default_message = '参数格式错误'


class RangeErrorException(BaseAPIException):
    """参数值范围错误异常"""
    status_code = 400
    error_code = 'E103'
    default_message = '参数值范围错误'


class AuthenticationException(BaseAPIException):
    """认证异常"""
    status_code = 401
    error_code = 'E010'
    default_message = '未登录或登录已过期'


class InvalidCredentialsException(AuthenticationException):
    """用户名或密码错误异常"""
    error_code = 'E011'
    default_message = '用户名或密码错误'


class PermissionException(BaseAPIException):
    """权限不足异常"""
    status_code = 403
    error_code = 'E020'
    default_message = '权限不足'


class NotFoundException(BaseAPIException):
    """资源不存在异常"""
    status_code = 404
    error_code = 'E030'
    default_message = '资源不存在'


class EmployeeNotFoundException(NotFoundException):
    """员工不存在异常"""
    error_code = 'E031'
    default_message = '员工不存在'


class ScheduleNotFoundException(NotFoundException):
    """排班不存在异常"""
    error_code = 'E032'
    default_message = '排班不存在'


class UserNotFoundException(NotFoundException):
    """用户不存在异常"""
    error_code = 'E033'
    default_message = '用户不存在'


class DuplicateException(BaseAPIException):
    """数据已存在异常"""
    status_code = 409
    error_code = 'E040'
    default_message = '数据已存在'


class UsernameExistsException(DuplicateException):
    """用户名已存在异常"""
    error_code = 'E041'
    default_message = '用户名已存在'


class StateNotAllowedException(BaseAPIException):
    """状态不允许异常"""
    status_code = 422
    error_code = 'E050'
    default_message = '当前状态不允许此操作'


class AlreadyProcessedException(StateNotAllowedException):
    """申请已被处理异常"""
    error_code = 'E051'
    default_message = '申请已被处理，无法重复操作'


class InvalidStateException(StateNotAllowedException):
    """状态无效异常"""
    error_code = 'E052'
    default_message = '只能操作草稿状态的记录'


class ServerException(BaseAPIException):
    """服务器异常"""
    status_code = 500
    error_code = 'E900'
    default_message = '服务器内部错误'


class DatabaseException(ServerException):
    """数据库操作失败异常"""
    error_code = 'E901'
    default_message = '数据操作失败'
```

**Step 2: 验证语法正确性**

```bash
cd backend && python -c "from utils.exceptions import *; print('All exceptions imported OK')"
```

---

## Task 3: 优化全局异常处理器支持错误码

**Files:**
- Modify: `backend/utils/handlers.py`

**Step 1: 查看现有处理器**

```bash
cat backend/utils/handlers.py
```

**Step 2: 更新 `_format_drf_response` 函数**

修改 `_format_drf_response` 函数以支持错误码：

```python
def _format_drf_response(exc, response, view_name: str) -> Response:
    """格式化 DRF 异常响应为统一格式"""
    # 记录错误日志
    if response.status_code >= 500:
        logger.error(f"服务器错误 in {view_name}: {str(exc)}", exc_info=True)
    elif response.status_code >= 400:
        logger.warning(f"客户端错误 in {view_name}: {str(exc)}")

    # 构建统一响应格式
    custom_response_data = {
        'code': response.status_code,
        'message': _get_error_message(exc),
        'data': None
    }

    # 处理错误详情
    if hasattr(exc, 'detail'):
        detail = exc.detail
        if isinstance(detail, dict):
            # 格式化字段错误
            formatted_errors = {}
            for field, errors in detail.items():
                if isinstance(errors, list):
                    formatted_errors[field] = errors[0] if errors else ''
                else:
                    formatted_errors[field] = str(errors)
            custom_response_data['errors'] = formatted_errors
        elif isinstance(detail, list) and detail:
            custom_response_data['errors'] = {'detail': detail[0] if detail else ''}
        elif isinstance(detail, str):
            custom_response_data['errors'] = {'detail': detail}

    response.data = custom_response_data
    return response
```

**Step 3: 添加自定义异常处理逻辑**

在 `custom_exception_handler` 函数中添加对 `BaseAPIException` 的处理：

```python
def custom_exception_handler(exc, context):
    """自定义全局异常处理器"""
    # 调用 DRF 默认异常处理
    response = exception_handler(exc, context)

    # 获取视图信息
    view = context.get('view')
    view_name = view.__class__.__name__ if view else 'UnknownView'

    # 检查是否是自定义异常
    if hasattr(exc, 'error_code'):
        logger.warning(f"自定义异常 in {view_name}: {exc.error_code} - {str(exc)}")
        return Response({
            'code': exc.error_code,
            'message': str(exc.detail),
            'detail': getattr(exc, 'detail', None),
            'data': None
        }, status=exc.status_code)

    if response is not None:
        return _format_drf_response(exc, response, view_name)

    # 处理 Django 特定异常
    if isinstance(exc, DjangoValidationError):
        logger.warning(f"Django 验证错误 in {view_name}: {str(exc)}")
        return Response({
            'code': 'E100',
            'message': '数据验证失败',
            'detail': str(exc),
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, DatabaseError):
        logger.error(f"数据库错误 in {view_name}: {str(exc)}", exc_info=True)
        return Response({
            'code': 'E901',
            'message': '数据操作失败',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 处理未捕获的异常
    logger.error(
        f"未捕获的异常 in {view_name}: {type(exc).__name__}: {str(exc)}",
        exc_info=True
    )
    return Response({
        'code': 'E900',
        'message': '服务器内部错误',
        'data': None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

**Step 4: 验证语法正确性**

```bash
cd backend && python -c "from utils.handlers import custom_exception_handler; print('OK')"
```

---

## Task 4: 测试异常处理流程

**Step 1: 启动 Django 服务器测试**

```bash
cd backend && python manage.py runserver 8000
```

**Step 2: 测试参数验证异常**

使用 curl 或 Postman 测试：

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ -H "Content-Type: application/json" -d '{}'
```

预期响应：
```json
{"code": "E100", "message": "参数验证失败", "errors": {...}, "data": null}
```

---

## Task 5-8: 改造 accounts/views.py 使用新的异常类

**Files:**
- Modify: `backend/accounts/views.py`

需要将以下手动返回错误的地方改为抛出异常：

1. `login` 方法（第 51-53 行）
2. `register` 方法（第 74 行）
3. `change_password` 方法（第 252-257 行）

**Step 1: 导入异常类**

在文件开头添加导入：

```python
from utils.exceptions import (
    ValidationException,
    InvalidCredentialsException,
    UsernameExistsException,
    PermissionException,
)
```

**Step 2: 修改 login 方法**

将：
```python
return ApiResponse.unauthorized(message='用户名或密码错误')
```

改为：
```python
raise InvalidCredentialsException('用户名或密码错误')
```

将：
```python
return ApiResponse.error(message='请求参数错误', errors=serializer.errors)
```

改为：
```python
raise ValidationException(detail=serializer.errors)
```

**Step 3: 修改 register 方法**

将：
```python
return ApiResponse.error(message='注册失败', errors=serializer.errors)
```

改为：
```python
raise ValidationException(detail=serializer.errors)
```

**Step 4: 修改 change_password 方法**

将：
```python
if not old_password or not new_password:
    return ApiResponse.error(message='请提供旧密码和新密码')
```

改为：
```python
if not old_password or not new_password:
    raise RequiredFieldException('请提供旧密码和新密码')
```

将：
```python
if user.password != old_password:
    return ApiResponse.unauthorized(message='旧密码错误')
```

改为：
```python
if user.password != old_password:
    raise InvalidCredentialsException('旧密码错误')
```

**Step 5: 验证**

```bash
cd backend && python -c "from accounts.views import UserViewSet; print('OK')"
```

---

## Task 9-12: 改造 employees/views.py 使用新的异常类

**Files:**
- Modify: `backend/employees/views.py`

**Step 1: 导入异常类**

```python
from utils.exceptions import (
    ValidationException,
    NotFoundException,
    EmployeeNotFoundException,
)
```

**Step 2: 修改 create/update 方法**

将手动错误返回改为抛出异常。

**Step 3: 验证**

```bash
cd backend && python -c "from employees.views import EmployeeProfileViewSet; print('OK')"
```

---

## Task 13-16: 改造 schedules/views.py 使用新的异常类

**Files:**
- Modify: `backend/schedules/views.py`

**Step 1: 导入异常类**

```python
from utils.exceptions import (
    ValidationException,
    NotFoundException,
    ScheduleNotFoundException,
    StateNotAllowedException,
    AlreadyProcessedException,
    RequiredFieldException,
)
```

**Step 2: 修改 batch_create, calendar_view, approve, my_requests 方法**

将手动返回错误改为抛出对应异常。

**Step 3: 验证**

```bash
cd backend && python -c "from schedules.views import ScheduleViewSet; print('OK')"
```

---

## Task 17-20: 改造 leaves/views.py 使用新的异常类

**Files:**
- Modify: `backend/leaves/views.py`

**Step 1: 导入异常类**

```python
from utils.exceptions import (
    ValidationException,
    NotFoundException,
    StateNotAllowedException,
    AlreadyProcessedException,
    RequiredFieldException,
    EmployeeNotFoundException,
)
```

**Step 2: 修改 my_requests, approve 方法**

**Step 3: 验证**

```bash
cd backend && python -c "from leaves.views import LeaveRequestViewSet; print('OK')"
```

---

## Task 21-24: 改造 attendance/views.py 使用新的异常类

**Files:**
- Modify: `backend/attendance/views.py`

**Step 1: 导入异常类**

```python
from utils.exceptions import (
    ValidationException,
    NotFoundException,
    EmployeeNotFoundException,
    StateNotAllowedException,
    RequiredFieldException,
)
```

**Step 2: 修改 clock_in, clock_out, my_attendance 等方法**

**Step 3: 验证**

```bash
cd backend && python -c "from attendance.views import AttendanceRecordViewSet; print('OK')"
```

---

## Task 25-28: 改造 salaries/views.py 使用新的异常类

**Files:**
- Modify: `backend/salaries/views.py`

**Step 1: 导入异常类**

```python
from utils.exceptions import (
    ValidationException,
    NotFoundException,
    StateNotAllowedException,
    AlreadyProcessedException,
    RequiredFieldException,
    EmployeeNotFoundException,
    DatabaseException,
)
```

**Step 2: 修改 generate_salary, adjust_salary, approve_appeal, my_salaries 方法**

**Step 3: 验证**

```bash
cd backend && python -c "from salaries.views import SalaryRecordViewSet; print('OK')"
```

---

## Task 29: 最终集成测试

**Step 1: 启动服务器**

```bash
cd backend && python manage.py runserver 8000
```

**Step 2: 测试各类异常**

```bash
# 测试参数验证
curl -X POST http://127.0.0.1:8000/api/accounts/login/ -H "Content-Type: application/json" -d '{}'

# 测试认证错误
curl -X POST http://127.0.0.1:8000/api/accounts/login/ -H "Content-Type: application/json" -d '{"username":"admin","password":"wrong"}'

# 测试资源不存在
curl http://127.0.0.1:8000/api/employees/99999/
```

**Step 3: 验证响应格式**

预期响应格式：
```json
{
  "code": "E100",
  "message": "参数验证失败",
  "detail": "...",
  "data": null
}
```

---

**Plan complete and saved to `docs/plans/2026-02-21-backend-validation-implementation-plan.md`.**

**Two execution options:**

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing_plans, batch execution with checkpoints

Which approach?
