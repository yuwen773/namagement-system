# 后端参数校验错误信息优化设计

## 背景

当前后端参数校验返回的错误信息包含过多技术细节，用户体验不佳。

### 当前问题

```json
{
    "code": 400,
    "message": "{'id_card': [ErrorDetail(string='身份证号不能为空', code='blank')], 'health_certificate_expiry': [ErrorDetail(string='健康证到期日期格式不正确，请使用 YYYY-MM-DD 格式', code='invalid')]}",
    "data": null
}
```

### 期望结果

```json
{
    "code": 400,
    "message": "身份证号不能为空",
    "data": null
}
```

## 问题分析

问题出在 `backend/utils/handlers.py` 的 `_get_error_message` 函数：

1. `ErrorDetail` 对象的 `string` 属性存储了人类可读的错误信息，但代码使用 `str(error.string)` 导致输出变成 `"'身份证号不能为空'"`
2. 返回格式包含字段名前缀（如 `id_card: `），用户不需要看到字段名

## 修复方案

修改 `extract_error_message` 函数：
- 正确提取 `ErrorDetail.string` 属性的值（直接返回，而不是转成字符串）

修改返回值逻辑：
- 只返回错误信息，不包含字段名前缀

## 影响范围

- 仅修改 `backend/utils/handlers.py`
- 所有 DRF 验证错误都会使用此格式
- 无需修改其他文件

## 测试验证

修复后，请求带验证错误的数据，验证返回的错误信息格式是否符合预期。
