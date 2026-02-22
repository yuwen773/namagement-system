# 问题总结：后端参数校验错误信息优化

## 问题描述

后端返回的参数校验错误信息包含过多技术细节，用户体验差。

### 原始输出
```json
{
    "code": 400,
    "message": "{'id_card': [ErrorDetail(string='身份证号不能为空', code='blank')]}",
    "data": null
}
```

### 期望输出
```json
{
    "code": 400,
    "message": "身份证号不能为空",
    "data": null
}
```

## 根因分析

1. **ErrorDetail 对象处理错误**：`handlers.py` 中使用 `str(error.string)` 导致输出 `"'身份证号不能为空'"`（带引号）
2. **返回格式多余**：错误信息包含字段名前缀（如 `id_card: `）
3. **前端重复处理**：部分组件手动解析 error 对象并显示，导致重复弹窗

## 修复内容

### 1. backend/utils/handlers.py
- 修改 `extract_error_message` 函数，正确提取 `ErrorDetail.string` 值
- 去掉字段名前缀，仅返回错误信息
- 统一所有异常处理使用 `_get_error_message`

### 2. frontend/src/api/request.js
- 简化错误处理 switch 语句，删除重复的 case 401

### 3. frontend/src/views/admin/EmployeeManageView.vue
- 删除复杂的错误解析逻辑
- 直接使用 `error.response?.data?.message`

### 4. frontend/src/views/admin/AttendanceManageView.vue
- 同样简化错误处理逻辑

## 验证结果

修复后，错误信息简洁明了：
- `身份证号不能为空`
- 不再包含字段名、code、data 等冗余信息
- 不再重复弹窗
