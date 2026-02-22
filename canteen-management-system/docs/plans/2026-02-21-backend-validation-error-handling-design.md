# 后端接口参数校验与异常处理规范设计

**日期**: 2026-02-21
**项目**: 食堂管理系统 (Canteen Management System)
**主题**: 后端接口参数校验与异常处理规范化

## 1. 背景

当前项目后端接口的异常处理存在以下问题：

1. **异常处理不一致**：部分视图使用 `raise_exception=True`，部分手动返回 `ApiResponse.error()`
2. **缺少业务错误码体系**：只有 HTTP 状态码，无法精确区分业务错误类型
3. **自定义异常未被使用**：已定义 `BusinessError` 等异常类，但视图层未使用

## 2. 设计目标

1. 统一异常处理方式：所有参数校验失败时抛出异常，由全局异常处理器统一处理
2. 建立详细的业务错误码体系，便于前端精确处理不同错误类型
3. 规范化错误消息格式，提升开发体验和调试效率

## 3. 错误码体系设计

### 3.1 错误码结构

```
{http_status}{error_code}
```

- HTTP 状态码：1 位，表示错误大类
- 错误代码：2-3 位，表示具体错误类型

### 3.2 错误码详细定义

| HTTP状态码 | 错误码范围 | 说明 |
|------------|------------|------|
| 400 | E100-E199 | 参数验证错误 |
| 401 | E010-E019 | 认证错误 |
| 403 | E020-E029 | 权限错误 |
| 404 | E030-E039 | 资源不存在 |
| 409 | E040-E049 | 业务冲突/重复 |
| 422 | E050-E059 | 业务状态不允许 |
| 500 | E900-E999 | 服务器错误 |

### 3.3 具体错误码

| 错误码 | 说明 | HTTP状态码 |
|--------|------|------------|
| E100 | 参数验证失败 | 400 |
| E101 | 缺少必需参数 | 400 |
| E102 | 参数格式错误 | 400 |
| E103 | 参数值范围错误 | 400 |
| E010 | 未登录或登录已过期 | 401 |
| E011 | 用户名或密码错误 | 401 |
| E020 | 权限不足 | 403 |
| E030 | 资源不存在 | 404 |
| E031 | 员工不存在 | 404 |
| E032 | 排班不存在 | 404 |
| E033 | 用户不存在 | 404 |
| E040 | 数据已存在 | 409 |
| E041 | 用户名已存在 | 409 |
| E050 | 当前状态不允许此操作 | 422 |
| E051 | 申请已被处理，无法重复操作 | 422 |
| E052 | 只能操作草稿状态的记录 | 422 |
| E900 | 服务器内部错误 | 500 |
| E901 | 数据操作失败 | 500 |

## 4. 异常类设计

### 4.1 异常基类

```python
class BaseAPIException(APIException):
    """API 异常基类"""
    status_code = 400
    error_code = 'E100'
    message = '操作失败'
    detail = None

    def __init__(self, message=None, detail=None):
        self.message = message or self.message
        self.detail = detail
        super().__init__(detail=self.message)
```

### 4.2 异常类层次

```
BaseAPIException
├── ValidationException (E100)
│   ├── RequiredFieldException (E101)
│   ├── FormatErrorException (E102)
│   └── RangeErrorException (E103)
├── AuthenticationException (E010)
│   └── InvalidCredentialsException (E011)
├── PermissionException (E020)
├── NotFoundException (E030)
│   ├── EmployeeNotFoundException (E031)
│   ├── ScheduleNotFoundException (E032)
│   └── UserNotFoundException (E033)
├── DuplicateException (E040)
│   └── UsernameExistsException (E041)
├── StateNotAllowedException (E050)
│   ├── AlreadyProcessedException (E051)
│   └── InvalidStateException (E052)
└── ServerException (E900)
    └── DatabaseException (E901)
```

## 5. 全局异常处理器设计

### 5.1 响应格式

```json
{
  "code": "E100",
  "message": "参数验证失败",
  "detail": "用户名不能为空",
  "data": null
}
```

### 5.2 处理器逻辑

1. 捕获所有未处理的异常
2. 判断异常类型，提取错误码和错误消息
3. 格式化响应并返回统一格式

## 6. 实施步骤

1. 增强 `utils/exceptions.py`：添加错误码和新的异常类体系
2. 优化 `utils/handlers.py`：支持新的错误码格式
3. 改造视图层：将手动返回错误改为抛出异常
4. 添加国际化支持（可选）：错误消息支持多语言

## 7. 兼容性说明

- 保持 `ApiResponse` 类不变，确保向后兼容
- 新旧错误格式可以共存，逐步迁移
- 前端需要适配新的错误码格式
