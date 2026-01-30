# 数据导入工作记录

> 更新日期: 2026-01-30

## 任务背景

**目标**: 将清洗后的 20,000 条菜谱数据导入到 MySQL 数据库

**输入文件**: `data-scripts/output/cleaned_20k_recipes.json`

**目标表**: `recipes`, `ingredients`, `recipe_ingredients`

---

## 导入脚本

**文件位置**: `data-scripts/importing/import_recipes.py`

**核心功能**:
- 批量插入优化（`bulk_create`）
- 食材自动分类（100+ 种食材规则）
- 食材名称标准化（截断超长名称）
- 食材去重（同一菜谱中相同食材只保留一个）
- 统计数据生成（点击量、收藏量）
- 进度显示和错误处理

---

## 遇到的问题与解决方案

### 问题 1: 食材名称超过字段长度限制

**错误信息**:
```
django.db.utils.DataError: (1406, "Data too long for column 'name' at row 1")
```

**原因**: 部分食材名称超过 100 字符（最长达 117 字符），这些名称包含了过多的用量说明。

**解决方案**: 添加 `normalize_ingredient_name()` 方法

```python
def normalize_ingredient_name(self, name):
    """
    标准化食材名称

    - 截断超过100字符的名称
    - 移除括号内的详细用量说明（保留主要名称）
    """
    if len(name) > 100:
        # 尝试提取括号前的主名称
        import re
        match = re.match(r'^([^\(（]+)', name)
        if match:
            main_name = match.group(1).strip()
            if 0 < len(main_name) <= 100:
                return main_name
        # 直接截断到100字符
        return name[:100].strip()
    return name
```

**结果**: 成功处理了 5 个超长食材名称。

---

### 问题 2: 同一菜谱中重复食材

**错误信息**:
```
django.db.utils.IntegrityError: (1062, "Duplicate entry '39915-13974' for key 'recipe_ingredients.unique_recipe_ingredient'")
```

**原因**: 同一菜谱中包含相同的食材（如多次使用"盐"），违反了唯一约束。

**解决方案**: 在创建食材关联时添加去重逻辑

```python
# 去重：同一菜谱中相同食材只保留第一个
seen_ingredients = set()
unique_ingredients = []
for ing_data in ingredients_data:
    ingredient_name = ing_data.get('name')
    if not ingredient_name:
        continue
    # 标准化食材名称（用于去重比较）
    normalized_name = self.normalize_ingredient_name(ingredient_name)
    if normalized_name not in seen_ingredients:
        seen_ingredients.add(normalized_name)
        unique_ingredients.append((ing_data, len(seen_ingredients) - 1))
```

**结果**: 成功去重，避免唯一约束冲突。

---

## 导入结果

### 最终统计

```
============================================================
导入完成！
============================================================
原始数据:     20,000 条
成功导入菜谱: 20,000 条
新增食材:     63,653 种
食材关联:     143,811 条
跳过记录:     0 条
============================================================
```

### 数据库验证

| 表名 | 记录数 | 说明 |
|:-----|:-------|:-----|
| recipes | 20,004 | 20,000 条导入 + 4 条测试数据 |
| ingredients | 63,661 | 63,653 种新增 + 8 种测试数据 |
| recipe_ingredients | 143,819 | 143,811 条新增 + 8 条测试数据 |

### 随机验证样本

```
名称:       凉拌竹丝鸡
菜系:       家常菜
难度:       中等
食材数:     13 种
点击量:     23,355
收藏量:     2,739
```

---

## 脚本改进总结

### 改进 1: 食材名称标准化

- **文件**: `import_recipes.py:340-365`
- **功能**: 智能处理超长食材名称
- **策略**: 优先提取括号前的主名称，否则直接截断

### 改进 2: 食材去重

- **文件**: `import_recipes.py:500-520`
- **功能**: 同一菜谱中相同食材只保留第一个
- **策略**: 使用 `set` 进行去重，基于标准化后的食材名称

---

## 使用方法

### 测试导入

```bash
cd data-scripts/importing

# SQLite 版本测试（推荐）
python test_import_sqlite.py
```

### 正式导入

```bash
cd data-scripts/importing

# 导入清洗后的数据
python import_recipes.py ../output/cleaned_20k_recipes.json
```

### 验证导入

```bash
cd backend

# 检查数据
python manage.py shell -c "
from recipes.models import Recipe
from ingredients.models import Ingredient
print(f'菜谱数: {Recipe.objects.count()}')
print(f'食材数: {Ingredient.objects.count()}')
"
```

---

## 相关文件

| 文件 | 说明 |
|:-----|:-----|
| `data-scripts/importing/import_recipes.py` | 主导入脚本 |
| `data-scripts/importing/test_import_sqlite.py` | SQLite 测试脚本 |
| `data-scripts/importing/README.md` | 使用文档 |
| `data-scripts/output/cleaned_20k_recipes.json` | 清洗后的数据 |
| `docs/data_cleaning.md` | 数据清洗记录 |

---

## 下一步

数据导入完成后，可以：

1. ✅ 验证数据完整性（已完成）
2. ⏭️ 运行 API 测试验证数据可用性
3. ⏭️ 开始阶段四：用户认证与权限系统

---

## 附录: 数据生成规则

| 数据项 | 生成规则 | 备注 |
|:------|:--------|:-----|
| 点击量 | 100-50000 随机数 | 如果数据中已有，使用原值 |
| 收藏量 | 点击量的 5%-20% | 如果数据中已有，使用原值 |
| 难度 | 简单 40%、中等 40%、困难 20% | 如果数据中已有，使用原值 |
| 食材分类 | 根据名称自动分类 | 内置 100+ 种食材分类规则 |
