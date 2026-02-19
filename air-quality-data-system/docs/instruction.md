# 后端开发指导文档 - API 错误提示优化

## 文档概述

本文档总结了项目中的 API 错误提示优化工作，提供了一套完整的开发规范和最佳实践，帮助开发者在未来开发中避免类似问题的二次返工。

**适用范围**：Django + DRF 后端项目
**更新时间**：2026-02-16

---

## 1. 问题分类与范畴

本次优化工作属于 **API 用户体验优化** 范畴，具体包括：

### 1.1 问题类型

| 问题类型 | 具体表现 | 影响范围 |
|---------|---------|---------|
| **国际化问题** | 错误消息为英文 | 用户无法理解 |
| **用户体验问题** | 错误消息生硬、技术化 | 用户不知道如何修正 |
| **信息泄露问题** | 暴露内部实现细节 | 暴露数据库字段名、模型名 |
| **一致性问题** | 不同端点错误提示风格不统一 | 用户体验混乱 |

### 1.2 涉及的文件层级

```
后端项目
├── models/           # 模型层 - 字段验证器消息
├── serializers/      # 序列化器层 - 字段错误消息配置
├── views/           # 视图层 - 业务错误处理
├── utils/           # 工具层 - 全局异常处理
└── settings.py      # 配置层 - DRF 全局配置
```

---

## 2. 根本原因分析

### 2.1 框架默认行为问题

**Django REST Framework 的默认行为：**

1. **验证器默认消息为英文**
   ```python
   # ❌ 问题代码
   RegexValidator(
       regex=r"^[0-9+\-() ]{6,20}$",
       message="Phone must be 6-20 chars: digits, spaces, + - ( ) only.",  # 英文
   )
   ```

2. **字段验证默认使用通用模板**
   - `required` → "This field is required."
   - `blank` → "This field may not be blank."
   - `min_length` → "Ensure this field has at least X characters."

3. **关联对象错误信息技术化**
   - 无效主键 → "Invalid pk '99999' - object does not exist."
   - 外键约束 → "Object with name already exists."

### 2.2 开发流程缺失

**常见开发疏漏：**

1. ❌ 直接使用模型字段名作为错误提示的参数
   ```python
   raise ValidationError("参数 'min_aqi' 格式错误")  # 暴露英文字段名
   ```

2. ❌ 未在序列化器中定义自定义错误消息
   ```python
   # ❌ 问题代码
   username = serializers.CharField(min_length=3)

   # ✅ 正确代码
   username = serializers.CharField(
       min_length=3,
       error_messages={"min_length": "用户名长度至少需要3位"}
   )
   ```

3. ❌ 业务逻辑错误消息不够明确
   ```python
   # ❌ 问题代码
   raise ValidationError("用户名已存在")

   # ✅ 正确代码
   raise ValidationError("该用户名已被注册，请更换其他用户名")
   ```

---

## 3. 错误提示设计原则

### 3.1 用户友好原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **明确性** | 清楚指出哪个字段有问题 | "请输入用户名" 而非 "此字段是必填项" |
| **可操作性** | 告诉用户如何修正 | "密码长度至少需要6位" 包含了具体的长度要求 |
| **避免术语** | 不使用技术术语 | "请选择文章分类" 而非 "请选择 category_id" |
| **中文优先** | 中文系统必须使用中文 | 全部使用简体中文 |

### 3.2 错误提示结构模板

```
[动词] + [字段中文名] + [要求/问题描述]

示例：
- "请输入用户名"（必填）
- "用户名长度至少需要3位"（长度验证）
- "请选择文章分类"（关联选择）
- "该用户名已被注册，请更换其他用户名"（业务冲突）
```

### 3.3 字段命名规范

**英文字段名 → 中文显示名映射：**

| 英文字段 | 中文显示 | 备注 |
|---------|---------|------|
| id | ID | 直接使用 |
| username | 用户名 | 完整翻译 |
| min_aqi | AQI最小值 | 添加单位说明 |
| population_type | 人群类型 | 完整翻译 |
| category_id | 文章分类 | 去掉_id后缀 |
| is_enabled | 启用状态 | 布尔字段加"状态" |

---

## 4. 实现规范

### 4.1 模型层（models.py）

**验证器消息规范：**

```python
from django.core.validators import RegexValidator

# ✅ 正确 - 中文消息
phone = models.CharField(
    max_length=20,
    null=True,
    blank=True,
    validators=[
        RegexValidator(
            regex=r"^[0-9+\-() ]{6,20}$",
            message="手机号格式不正确，应为6-20位数字，可包含空格和+-()符号",
        )
    ],
)

# ❌ 错误 - 英文消息
phone = models.CharField(
    validators=[
        RegexValidator(
            regex=r"^[0-9+\-() ]{6,20}$",
            message="Phone must be 6-20 chars: digits, spaces, + - ( ) only.",
        )
    ],
)
```

### 4.2 序列化器层（serializers.py）

**字段错误消息配置规范：**

```python
# ✅ 正确 - 完整的错误消息配置
username = serializers.CharField(
    min_length=3,
    max_length=20,
    error_messages={
        "required": "请输入用户名",
        "blank": "用户名不能为空",
        "min_length": "用户名长度至少需要3位",
        "max_length": "用户名长度不能超过20位"
    }
)

# ✅ 正确 - EmailField 的错误消息
email = serializers.EmailField(
    error_messages={
        "required": "请输入邮箱地址",
        "blank": "邮箱地址不能为空",
        "invalid": "请输入有效的邮箱地址"
    }
)

# ✅ 正确 - ChoiceField 的错误消息
role = serializers.ChoiceField(
    choices=User.Role.choices,
    error_messages={
        "required": "请选择用户角色",
        "invalid_choice": "用户角色无效"
    }
)

# ✅ 正确 - PrimaryKeyRelatedField 的错误消息
category = serializers.PrimaryKeyRelatedField(
    queryset=ArticleCategory.objects.all(),
    error_messages={
        "required": "请选择文章分类",
        "null": "请选择文章分类",
        "does_not_exist": "所选分类不存在，请重新选择有效的分类"
    }
)
```

**自定义验证方法规范：**

```python
# ✅ 正确 - 明确的错误消息
def validate_username(self, value):
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError("该用户名已被注册，请更换其他用户名")
    return value

# ❌ 错误 - 消息不够明确
def validate_username(self, value):
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError("用户名已存在")
    return value
```

### 4.3 视图层（views.py）

**字段名翻译规范：**

```python
# ✅ 正确 - 使用中文字段名
from utils.exception_handler import translate_field_name

def _parse_int_payload(value, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        # 使用翻译后的字段名
        translated_field = translate_field_name(field)
        raise ValidationError(f"{translated_field}格式错误，应为整数", field=field)
```

**业务错误消息规范：**

```python
# ✅ 正确 - 友好的业务错误消息
def _translate_validation_error(message: str) -> str:
    """翻译常见的验证错误消息为中文"""
    translations = {
        "AQI ranges must not overlap within the same population_type.":
            "该人群类型下已存在相同或重叠的 AQI 范围，请检查并调整范围。",
        "min_aqi must be <= max_aqi.":
            "AQI 最小值不能大于最大值。",
    }
    return translations.get(message, message)

# ✅ 正确 - 捕获 Django ValidationError 并转换
try:
    instance = serializer.save()
except DjangoValidationError as e:
    message = _translate_validation_error(str(e))
    raise ValidationError(message=message, field=None)
```

### 4.4 工具层（utils/exception_handler.py）

**字段名映射表：**

```python
# ✅ 正确 - 维护完整的字段名映射
FIELD_NAME_MAP = {
    # 通用字段
    "id": "ID",
    "name": "名称",
    "title": "标题",
    "content": "内容",
    "status": "状态",

    # 用户相关
    "username": "用户名",
    "password": "密码",
    "email": "邮箱",
    "phone": "手机号",

    # 规则相关
    "rule_name": "规则名称",
    "min_aqi": "AQI最小值",
    "max_aqi": "AQI最大值",
    "population_type": "人群类型",
    "advice": "防护建议",

    # 文章相关
    "category_id": "文章分类",
    "category": "文章分类",

    # 操作字段
    "ids": "ID列表",
    "keyword": "关键词",
    "page": "页码",
    "page_size": "每页数量",
}

def translate_field_name(field_name: str) -> str:
    """将英文字段名翻译为中文"""
    return FIELD_NAME_MAP.get(field_name, field_name)
```

---

## 5. 开发检查清单

### 5.1 新增 API 端点时

- [ ] 确认所有必填字段有友好的 `required` 错误消息
- [ ] 确认所有验证规则有对应的中文错误消息
- [ ] 确认关联对象错误消息指向具体资源（如"所选分类不存在"）
- [ ] 确认业务冲突错误消息包含解决方案提示
- [ ] 在 `FIELD_NAME_MAP` 中添加新字段的中文映射

### 5.2 新增模型字段时

- [ ] 字段验证器使用中文错误消息
- [ ] 如果是外键，错误消息说明具体资源类型
- [ ] 如果有格式要求，错误消息包含正确格式说明
- [ ] 布尔字段的错误消息避免技术术语

### 5.3 新增序列化器时

- [ ] 为每个字段添加 `error_messages` 配置
- [ ] 至少包含：`required`、`blank`、`invalid` 的中文消息
- [ ] 数值字段包含 `min_value`、`max_value` 的消息
- [ ] 字符串字段包含 `min_length`、`max_length` 的消息
- [ ] 自定义 `validate_*` 方法的错误消息友好明确

### 5.4 代码审查要点

**审查时的检查项：**

```python
# ⚠️ 需要关注的代码模式
1. serializers.CharField(min_length=X)  # 缺少 error_messages
2. serializers.EmailField()              # 缺少 error_messages
3. raise ValidationError("xxx exists")   # 消息可以更友好
4. f"参数 '{field}' xxx"                 # 直接使用英文字段名
5. RegexValidator(message="English...") # 验证器消息是英文
```

---

## 6. 常见错误消息模板库

### 6.1 通用验证消息

```python
# 必填字段
"required": "请输入{字段名}"

# 为空检查
"blank": "{字段名}不能为空"

# 长度验证
"min_length": "{字段名}长度至少需要{n}位"
"max_length": "{字段名}长度不能超过{n}字"

# 数值验证
"min_value": "{字段名}不能小于{value}"
"max_value": "{字段名}不能大于{value}"
"invalid": "{字段名}格式错误，请输入有效值"

# 选择验证
"invalid_choice": "{字段名}无效，可选值：{选项列表}"
"does_not_exist": "所选{资源类型}不存在，请重新选择"
```

### 6.2 业务验证消息

```python
# 唯一性冲突
"该{资源}已存在，请使用其他{标识符}"

# 范围重叠
"该{范围类型}下已存在相同或重叠的范围，请调整范围"

# 关联依赖
"该{资源}下存在{关联资源}，无法删除"
"该{资源}下还有{关联资源}，请先处理相关{关联资源}后再删除{资源}"

# 权限检查
"您没有权限访问此资源"
"您没有权限执行此操作"
```

### 6.3 关联对象错误

```python
# 分类相关
"请选择文章分类"
"所选分类不存在，请重新选择有效的分类"
"该分类名称已存在，请使用其他名称"
"该分类下还有文章，请先移动或删除相关文章后再删除分类"

# 用户相关
"该用户名已被注册，请更换其他用户名"
"用户不存在或已被禁用"
"用户已被禁用"
```

---

## 7. 工具与辅助代码

### 7.1 错误消息测试脚本

```python
# backend/utils/test_error_messages.py
def test_serializer_error_messages():
    """测试序列化器错误消息是否为中文"""
    from apps.accounts.serializers import RegisterSerializer

    # 测试缺少必填字段
    serializer = RegisterSerializer(data={})
    if not serializer.is_valid():
        for field, errors in serializer.errors.items():
            for error in errors:
                # 检查是否包含中文字符
                assert any('\u4e00' <= c <= '\u9fff' for c in error), \
                    f"{field} 错误消息不是中文: {error}"
                # 检查是否包含英文技术术语
                assert 'This field' not in error, \
                    f"{field} 使用了 DRF 默认英文消息"
```

### 7.2 字段名映射生成脚本

```python
# backend/utils/generate_field_map.py
def generate_field_map_from_models():
    """从所有模型生成字段名映射表"""
    from django.apps import apps

    field_map = {}
    for model in apps.get_app_config('accounts').get_models():
        for field in model._meta.get_fields():
            field_name = field.name
            # 尝试从 verbose_name 获取中文
            if hasattr(field, 'verbose_name') and field.verbose_name:
                field_map[field_name] = str(field.verbose_name)

    return field_map
```

---

## 8. 相关文件清单

### 8.1 本次优化涉及的文件

| 文件 | 修改内容 | 重要性 |
|------|---------|--------|
| `backend/apps/accounts/models.py` | 手机号验证器消息 | ⭐⭐⭐ |
| `backend/apps/accounts/serializers.py` | 登录/注册/用户管理序列化器 | ⭐⭐⭐⭐⭐ |
| `backend/apps/rules/serializers.py` | 规则序列化器 | ⭐⭐⭐⭐⭐ |
| `backend/apps/articles/serializers.py` | 文章/分类序列化器 | ⭐⭐⭐⭐⭐ |
| `backend/apps/rules/views.py` | 业务错误消息翻译 | ⭐⭐⭐⭐ |
| `backend/utils/exception_handler.py` | 字段名映射表 | ⭐⭐⭐⭐ |

### 8.2 参考文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 架构文档 | `memory-bank/architecture.md` | 项目架构说明 |
| 产品需求 | `memory-bank/PRD.md` | 功能需求说明 |
| API 文档 | `API_DOCS.md` | 接口文档 |

---

## 9. 总结与建议

### 9.1 核心原则

1. **用户体验优先** - 错误提示是用户体验的重要组成部分
2. **中文优先** - 中文系统必须使用中文错误消息
3. **明确具体** - 错误消息必须清楚指出问题和解决方案
4. **一致性** - 同类错误使用统一的措辞风格
5. **可维护性** - 使用映射表和翻译函数，便于统一管理

### 9.2 开发建议

1. **在创建序列化器时同步添加 error_messages** - 避免后期返工
2. **在创建验证器时使用中文消息** - 模型层就做好国际化
3. **使用翻译函数而不是硬编码中文** - 便于后续维护
4. **定期进行错误消息审查** - 在代码审查时检查错误提示
5. **建立错误消息单元测试** - 防止回归

### 9.3 后续改进方向

1. **提取错误消息到配置文件** - 便于统一管理和修改
2. **支持多语言切换** - 为国际化做准备
3. **建立错误消息组件库** - 常见错误消息模板
4. **自动化测试覆盖** - 检测非中文错误消息

---

## 附录：快速参考

### A. 完整的 Serializer 字段模板

```python
class ExampleSerializer(serializers.ModelSerializer):
    # 文本字段
    name = serializers.CharField(
        max_length=100,
        error_messages={
            "required": "请输入名称",
            "blank": "名称不能为空",
            "max_length": "名称长度不能超过100字"
        }
    )

    # 必填文本字段
    title = serializers.CharField(
        max_length=255,
        error_messages={
            "required": "请输入标题",
            "blank": "标题不能为空",
            "max_length": "标题过长，请控制在255字以内"
        }
    )

    # 邮箱字段
    email = serializers.EmailField(
        error_messages={
            "required": "请输入邮箱地址",
            "blank": "邮箱地址不能为空",
            "invalid": "请输入有效的邮箱地址"
        }
    )

    # 整数字段
    age = serializers.IntegerField(
        error_messages={
            "required": "请输入年龄",
            "invalid": "年龄格式错误，请输入整数"
        }
    )

    # 选择字段
    status = serializers.ChoiceField(
        choices=["ACTIVE", "INACTIVE"],
        error_messages={
            "required": "请选择状态",
            "invalid_choice": "状态无效，可选值：ACTIVE、INACTIVE"
        }
    )

    # 关联对象字段
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            "required": "请选择分类",
            "null": "请选择分类",
            "does_not_exist": "所选分类不存在，请重新选择"
        }
    )

    # 布尔字段
    is_enabled = serializers.BooleanField(
        required=False,
        error_messages={"invalid": "启用状态格式错误"}
    )

    # 可选字段
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        error_messages={"max_length": "手机号长度不能超过20位"}
    )
```

### B. 常用 DRF 错误类型与对应 error_messages 键

```python
# CharField
error_messages = {
    "required": "请输入{字段}",
    "blank": "{字段}不能为空",
    "max_length": "{字段}长度不能超过{n}字",
    "min_length": "{字段}长度至少需要{n}位",
    "invalid": "{字段}格式错误",
}

# EmailField
error_messages = {
    "required": "请输入邮箱地址",
    "blank": "邮箱地址不能为空",
    "invalid": "请输入有效的邮箱地址",
}

# IntegerField
error_messages = {
    "required": "请输入{字段}",
    "invalid": "{字段}格式错误，请输入整数",
    "max_value": "{字段}不能大于{value}",
    "min_value": "{字段}不能小于{value}",
}

# ChoiceField
error_messages = {
    "required": "请选择{字段}",
    "invalid_choice": "{字段}无效，可选值：{choices}",
}

# BooleanField
error_messages = {
    "invalid": "{字段}格式错误",
}

# PrimaryKeyRelatedField
error_messages = {
    "required": "请选择{关联资源}",
    "null": "请选择{关联资源}",
    "does_not_exist": "所选{关联资源}不存在",
}
```

---

**文档维护：**
本文档应随着项目的迭代持续更新。当发现新的错误提示问题或改进点时，请及时更新本文档。

**文档版本：** v1.0
**创建日期：** 2026-02-16
**维护者：** 开发团队
